# -*- coding: utf-8 -*-
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.conf import settings

from myproject.wordlists.models import WordList
from myproject.wordlists.forms import WordListForm

import os
import re

####################################################################################################

def delete_wordlist(wordlists, delete=True, merge_to=None):
    if merge_to:
        merge_to_wl = WordList.objects.get(list_id=merge_to)

    try:
        number_of_objects_to_delete = WordList.objects.filter(list_id__in=wordlists).count()
        for wl in WordList.objects.filter(list_id__in=wordlists):
            if merge_to:
                merge_to_wl.merge(wl)
            if delete:
                wl.delete()
                WordList.objects.filter( list_id__in=wordlists ).delete()
    except Exception, e:
        return {
            'message':  "Error: %s" % e,
            'success': False
        }

    if number_of_objects_to_delete != 1:
        plural = "s"
    else:
        plural = ""

    if merge_to:
        if delete:
            action_name = 'merged and deleted'
        else:
            action_name = 'merged'
    else:
        action_name = 'deleted'

    return {
        'message':  "%s wordlist%s %s" % (number_of_objects_to_delete, plural, action_name),
        'success': True
    }


def get_primary_wordlist(user, language):
    title = settings.VOCABULARY_NAME.get( language, 'Basic Vocabulary (%s)'%language )
    description = settings.VOCABULARY_DESCRIPTION.get( language, 'That is a basic vocabulary of %s'%language )
    color = settings.BASIC_VOCABULARY_COLOR.get( language, '$ffff99' )

    if WordList.objects.filter(language=language, user=user, primary=True).count() == 0:
        new_wordlist = WordList(title=title, description=description, color=color, language=language, user=user, primary=True)
        new_wordlist.save()
        return new_wordlist
    else:
        found_wordlist = WordList.objects.get(language=language, user=user, primary=True)
        return found_wordlist


@login_required
def list_wordlists(request):
    message = None
    if request.method == 'POST':

        wordlists = []
        for k in request.POST.keys():
            if not k.startswith('cb_'):
                continue
            wordlists.append( k[3:] )

        if 'delete' in request.POST:
            message = delete_wordlist(wordlists)
        elif 'blind_merge_keep' in request.POST or 'blind_merge_delete' in request.POST:
            if 'blind_merge_keep' in request.POST:
                merge_to = request.POST['blind_merge_keep']
                delete = False
            else:
                merge_to = request.POST['blind_merge_delete']
                delete = True

            try:
                message = delete_wordlist(wordlists, delete=delete, merge_to=merge_to)
            except Exception, e:
                message = e
        elif 'attended_merge' in request.POST:
            merge_to = request.POST['attended_merge']
            return HttpResponseRedirect( reverse( 'attended_merge', args=( "+".join(wordlists), merge_to ) ) )

    wordlists = WordList.objects.filter(user=request.user)
    return render_to_response(
        'list_wordlists.html',
        {'wordlists': wordlists, 'message': message,},
        context_instance=RequestContext(request)
    )

@login_required
def add_new_wordlist(request, list_id=None):
    # Handle file upload
    if list_id:
        wordlist = get_object_or_404(WordList, list_id=list_id)
        if wordlist.user != request.user:
            return HttpResponseForbidden()
        caption = 'Update wordlist info'
        button = 'Update'
        url = reverse('myproject.wordlists.views.add_new_wordlist', args=[list_id])
    else:
        caption = 'Add new wordlist'
        button = 'Add'
        url = reverse('myproject.wordlists.views.add_new_wordlist')
        wordlist = None

    if request.method == 'POST':
        if wordlist:
            form = WordListForm(request.POST, request.FILES, instance=wordlist)
        else:
            form = WordListForm(request.POST, request.FILES)
        if form.is_valid():
            if wordlist:
                wordlist.title = form.cleaned_data['title']
                wordlist.description = form.cleaned_data['description']
                wordlist.language = form.cleaned_data['language']
                wordlist.color = form.cleaned_data['color']
            else:
                wordlist = WordList(
                    title = form.cleaned_data['title'],
                    description = form.cleaned_data['description'],
                    language = form.cleaned_data['language'],
                    color = form.cleaned_data['color'],
                    user = request.user,
                )
            wordlist.save()
            return HttpResponseRedirect(reverse('myproject.wordlists.views.list_wordlists'))
    else:
        if wordlist:
            form = WordListForm(instance=wordlist)
        else:
            form = WordListForm()

    return render_to_response(
        'add_new_wordlist.html',
        {'form': form, 'button': button,'url':url, 'caption': caption},
        context_instance=RequestContext(request)
    )

@login_required
def attended_merge_wordlist(request):
    pass

@login_required
def show(request, list_id):
    wl = get_object_or_404(WordList, list_id=list_id)
    grouped_words, tags, translation = wl.grouped_words()
    answer = ""
    for i in sorted(grouped_words.keys()):
        answer += "##" + i + '##' + tags.get(i, '') + '##' + translation.get(i, '') + "\n"
        answer += "\n".join( grouped_words[i] ) + "\n"
    return HttpResponse(answer, content_type='text/plain; charset=utf-8')

@login_required
def add_words(request, list_id):
    wl = get_object_or_404(WordList, list_id=list_id)
    if wl.user != request.user:
        return HttpResponseForbidden()

    message = None
    if request.method == 'POST':
        text = request.POST.get('add_words', '')
        words = re.sub('[^a-zA-ZäöëüßÄËÖÜß \n]', '', text).split()
        result = wl.save_words(words)
        if result:
            message = {
                'message':  'Words are added.',
                'success': result,
            }
        else:
            message = {
                'message':  'Words were not added. Some error occured',
                'success': result,
            }

    response = {
        'list':       wl,
        'message': message,
    }

    return render_to_response(
        'add_words.html',
        response,
        context_instance=RequestContext(request)
    )
