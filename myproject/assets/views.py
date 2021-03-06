# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET

import django.middleware.csrf

from django.contrib.auth.decorators import login_required


from myproject.assets.models import Document
from myproject.assets.forms import DocumentForm

from myproject.wordlists.models import WordList
from myproject.wordlists.views import get_primary_wordlist

from django.conf import settings

import json

import sys
import os
import subprocess

from myproject.micr.Translator.TranslateAPI import MicrosoftTranslatorClient
from django.shortcuts import render_to_response


def frequency(self):
	client = MicrosoftTranslatorClient('client_id', 'client_secret')
	Translation = client.TranslateText('Hello Jessica, this is what I have been working on', 'en', 'fr')
	return render_to_response('translate.html', {'translation_here': Translation})

def trigger_converter(doc_id):
    print [sys.executable, settings.PATH_TO_CONVERTER, doc_id]
    subprocess.Popen([sys.executable, settings.PATH_TO_CONVERTER, doc_id])

@login_required
def list(request):
    ## Handle file upload
    #if request.method == 'POST':
    #    form = DocumentForm(request.POST, request.FILES)
    #    if form.is_valid():
    #        newdoc = Document(
    #            docfile = request.FILES['docfile'],
    #            title = form.cleaned_data['title'],
    #        )
    #        newdoc.save()

    #        # Redirect to the document list after POST
    #        return HttpResponseRedirect(reverse('myproject.assets.views.list'))
    #else:
    #    form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents,},
        context_instance=RequestContext(request)
    )

@login_required
def upload(request):

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(
                docfile = request.FILES['docfile'],
                title = form.cleaned_data['title'],
                user = request.user,
            )
            newdoc.save()
            print "asset is uploaded"
            print "converting it"
            print newdoc.doc_id
            trigger_converter(newdoc.doc_id)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.assets.views.list'))
    else:
        form = DocumentForm()

    return render_to_response(
        'upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

@login_required
def converted(request, doc_id):
    filename = os.path.join(settings.PATH_TO_CONVERTED, doc_id, 'text')
    if '/' in doc_id or not os.path.exists(filename):
        filename = '/dev/null'
    return HttpResponse(file(filename), content_type='text/plain; charset=utf-8')

@login_required
def words(request, doc_id):
    filename = os.path.join(settings.PATH_TO_CONVERTED, doc_id, words)
    if '/' in doc_id or not os.path.exists(filename):
        filename = '/dev/null'
    return HttpResponse(file(filename), content_type='text/plain; charset=utf-8')

def load_words_in_lists(user, language):

    words_in_lists = {}
    for wl in WordList.objects.filter(user=user, language=language):
        for word in wl.load_words():
            if word in words_in_lists:
                words_in_lists[word].append( wl.list_id )
            else:
                words_in_lists[word] = [ wl.list_id ]

    return words_in_lists

    
def get_words_list(doc_id, words_in_lists=None, known_words=None):

    if words_in_lists is None:
        words_in_lists = {}

    f = os.path.join(settings.PATH_TO_CONVERTED, str(doc_id), 'words')
    if not os.path.exists(f):
        return []
    a = open(f).read()

    res = []
    for i, line in enumerate(a.splitlines()):
        if ' ' not in line:
            continue
        if line.startswith('#') and not line.startswith('##'):
            continue
        if line.startswith('##'):
            line = line[2:]
            group_total = True
        else:
            group_total = False

        if '##' in line:
            try:
                line, tags, translation = line.split('##')
                tags = "/".join(tags.split())
            except:
                tags = ''
                translation = ''
        else:
            translation = None
            tags = None

        x, y = line.split()

        if known_words and y in known_words:
            continue

        res.append({
            'count':    x,
            'word':     y,
            'examples': '',
            'lists':    words_in_lists.get(y, []),
            'group_total': group_total,
            'translation': translation,
            'tags': tags,
        })
        if i > 1000:
            break
    return res

def get_words_list_from_lists(lists, words_in_lists=None, known_words=None):
    count = {}
    tags = {}
    translation = {}

    words = []
    for list_id in lists:
        try:
            l = WordList.objects.get(list_id=list_id)
        except:
            continue

        grouped_words, _tags, _translation = l.grouped_words()
        tags.update( _tags )
        translation.update( _translation )

        for nword, words in grouped_words.items():
            if nword not in count:
                count[nword] = words
            else:
                count[nword] += words

    res = []
    for nword in count:
        for i, w in enumerate([nword] + count[nword]):
            item = {
                'count': "", #len(count[nword]) if i==0 else 1,
                'word':  w,
                'lists': words_in_lists.get( w, [] ),
                'group_total': i == 0,
            }
            if i == 0:
                item['translation'] = translation.get(w, '')
                item['tags'] = '/'.join( tags.get(w, '').split() )

            res.append(item)

    return res
            

def get_lists_list(language):
    return WordList.objects.filter(language=language, primary=False)

def load_known_words(user, lang, list_id=None):
    if list_id is None:
        wl = get_primary_wordlist(user, lang)
    else:
        try:
            wl = WordList.get(list_id=list_id)
        except:
            wl = None

    return wl.load_words()

def save_words(saved_words, user, lang, list_id=None):
    if not list_id:
        wl = get_primary_wordlist(user, lang)
    else:
        try:
            wl = WordList.objects.get(list_id=list_id)
        except Exception, e:
            print e
            return False

    return wl.save_words(saved_words)

@login_required
def attended_merge(request, lists, primary_list):
    return mark_words( request, lists, list_id=primary_list, processing_lists=True  )

@login_required
def mark_words(request, to_process, list_id=None, processing_lists=False, show_list=False):

    first_list = None
    if processing_lists:
        if type(to_process) == type(""):
            lists_ids = to_process.replace('+', ' ').split()
        else:
            lists_ids = to_process

        if list_id:
            main_list = get_object_or_404(WordList, list_id=list_id)
        else:
            first_list = get_object_or_404(WordList, list_id=lists_ids[0])
            main_list = get_object_or_404(WordList, primary=True, language=first_list.language, user=request.user)
        language = main_list.language
        document_or_list = main_list
    else:
        doc_id = to_process
        document = get_object_or_404(Document, doc_id=doc_id)
        language = document.language
        document_or_list = document

    if request.method == 'POST':
        data = json.loads( request.POST['data'] )
        result = save_words(data['selected_words'], request.user, language, list_id or (processing_lists and main_list.list_id))
        response_data = {
            'result':   result,
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if processing_lists:
        known_words = main_list.load_words()
    else:
        known_words = load_known_words(request.user, language)

    words_in_lists = load_words_in_lists(request.user, language)

    if processing_lists:
        words_list = get_words_list_from_lists( lists_ids, known_words=known_words, words_in_lists=words_in_lists )
    else:
        words_list = get_words_list(doc_id, known_words=known_words, words_in_lists=words_in_lists)

    lists_list = get_lists_list( language )

    django_data = {
        'url_translate': reverse('myproject.assets.views.translate', args=[language, '']),
        'csrf_token': django.middleware.csrf.get_token(request),
    }

    if not processing_lists:
        django_data.update({
            'doc_id': doc_id,
            'url_grep': reverse('myproject.assets.views.grep', args=[doc_id, '']),
            'url_marked_words': reverse('myproject.assets.views.mark_words', args=[doc_id]),
        })
    else:
        django_data.update({
            'url_marked_words': reverse('attended_merge', args=[to_process, list_id]),
        })

    params = { 
            'lists': lists_list,
            'words': words_list,
            'document': first_list if show_list else document_or_list,
            'django_data': mark_safe(json.dumps(django_data)),
            'url_add_new_wordlist': reverse('myproject.wordlists.views.add_new_wordlist'),
            'doing_merge': not show_list and processing_lists,
            'show_list': show_list,
    }

    return render_to_response(
        'mark-words.html',
        params,
        context_instance=RequestContext(request)
    )

@login_required
def show_list(request, list_to_show):
    return mark_words(request, [list_to_show], list_id=None, processing_lists=True, show_list=True)

@login_required
def grep(request, doc_id, keyword, start=None, step=5, return_dict=False):
    f = os.path.join(settings.PATH_TO_CONVERTED, doc_id, 'text')

    keyword = keyword.strip()
    p = subprocess.Popen([settings.PATH_TO_GREP, keyword, f], stdout=subprocess.PIPE)
    sentences = [ x.strip() for x in p.communicate()[0].replace(r'[35;1m', '<b>').replace(r'[0m', '</b>').splitlines() ]
    sentences = [ x for x in sentences if x != "" ]

    try:
        start = int(start)
    except:
        start = 0

    if start < len(sentences):
        sentences = sentences[start:]
    else:
        sentences = []

    if len(sentences) > step:
        sentences = sentences[:step]
        have_more = True
    else:
        have_more = False

    response_data = {
        'sentences': sentences,
        'found':    len(sentences) > 0,
        'more':     have_more,
    }
    if return_dict:
        return response_data

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def translate(request, lang, word, return_dict=False):

    from_lang = lang
    to_lang = 'ru'
    word = word.strip()
    p = subprocess.Popen([settings.PATH_TO_TRANSLATE, from_lang, to_lang, word.strip()], stdout=subprocess.PIPE)

    output = p.communicate()[0].decode('utf8')

    translated = False
    translation = []
    show = True
    header = True
    for line in output.splitlines():
        if 'Nothing similar to' in line:
            translated = False
        if line.lower() == '-->'+word.lower():
            show = True
            translated = True
            continue
        if line.startswith('-->'):
            if show:
                show = False
            continue
        if 'items, similar to' in line:
            continue
        if line.strip() == '' and header:
            continue
        header = False
        if show:
            translation.append( line )

    response_data = {
        'translation': "\n".join(translation),
        'translated': translated,
        'language_from': from_lang,
        'language_to': to_lang,
    }
    if return_dict:
        return response_data

    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json; charset=utf8")

def search_dictionary(request, q):
    langs = [
        'en', 'de', 'fr', 'es'
    ]
    res = []
    for w in q:
        for lang in langs:
            t = translate(request, lang, w, return_dict=True)
            if t['translated']:
                res.append(t)
    print res
    return res

def search_wordlists(request, q):
    res = []
    for wl in WordList.objects.filter(user=request.user):
        if wl.has_word(q):
            res.append(wl)
    return res

def search_assets(request, q):
    res = []
    for doc in Document.objects.filter(user=request.user):
        what_found = grep(request, doc.doc_id, " ".join(q), return_dict=True)
        if what_found['found']:
            res.append({
                'doc': doc,
                'found': what_found,
            })

    return res

@login_required
@require_GET
def search(request):
    query = request.GET.get('q')

    if not query:
        return render_to_response("search.html", {}, context_instance=RequestContext(request))

    q = query.split()

    translation = search_dictionary(request, q)

    wordlists = search_wordlists(request, q)
    if len(wordlists) == 0:
        wordlists = None

    assets = search_assets(request, q) 

    params = { 
        'query': query,
        'translation': translation,
        'wordlists': wordlists,
        'assets': assets,
    }
    return render_to_response(
        "search.html",
        params,
        context_instance=RequestContext(request),
    )
