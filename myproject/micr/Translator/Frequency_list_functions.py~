# -*- coding: utf-8 -*-

import re
import codecs
#from django.utils.encoding import smart_str
import collections
import os
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
import urllib2
import urllib
import nltk.data
from myproject.micr.Translator.mstranslator.client import MSTranslator
from myproject.micr.Translator.mstranslator.client import MSTranslatorAccessKey
import requests
from lxml import etree
from django.shortcuts import render_to_response
from urllib import urlencode
from urllib2 import Request, urlopen, URLError
import json
import os
import xml.etree.ElementTree as ET
from urllib2 import Request, urlopen, URLError
from httplib import HTTPResponse
import sys
from io import StringIO
from datetime import datetime, timedelta

def docsplitter(Document):
    SourceTextArray = []
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(Document)
    data = fp.read()
    data = data.decode('utf-8')
    SourceTextArray.append(tokenizer.tokenize(data))
    SourceTextArray = SourceTextArray[0]
    return SourceTextArray

def Create_xml(Array, from_language, to_language):
    # Creates an XML tree containing all of the information that Microsoft API needs to translate the Array
    root = etree.Element('TranslateArrayRequest')
    AppId = etree.SubElement(root, 'AppId')
    From = etree.SubElement(root, 'From')
    From.text = str(from_language)
    Options = etree.SubElement(root, 'Options')
    Category = etree.SubElement(Options, 'Category', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    ContentType = etree.SubElement(Options, 'ContentType', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    ContentType.text = 'text/plain'
    ReservedFlags = etree.SubElement(Options, 'ReservedFlags', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    State = etree.SubElement(Options, 'State', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    Uri = etree.SubElement(Options, 'Uri', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    User = etree.SubElement(Options,'User', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    Texts = etree.SubElement(root, 'Texts')
    for i in Array:
        string = etree.SubElement(Texts, 'string', xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays")
        i = i.encode('utf-8')
        i = unicode(i, 'utf-8', errors='replace')
        string.text = i
        # Changed the above from str(i) to i
    To = etree.SubElement(root, 'To')
    To.text = str(to_language)
    s = etree.tostring(root, xml_declaration=True, pretty_print=True, encoding='UTF-8')
    # Returns the XML back to the function as a string
    return s

def maketranslate(msarray):
    client_id = '263ee1af-8087-4592-bf85-5941238bdab6'
    client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='
    #Client secret and ID are linked to my Microsoft account, and never change.
    MS_TRANSLATOR_KEY = MSTranslatorAccessKey(client_id, client_secret)
    key = MS_TRANSLATOR_KEY
    translator = MSTranslator(key)
    headers = {'Authorization': translator.get_authorization_string(), 'content-type': 'application/xml'}
    XML_Doc = Create_xml(Array=msarray, from_language = 'en', to_language = 'de')
    data = XML_Doc
    W = requests.post(url='http://api.microsofttranslator.com/V2/Http.svc/TranslateArray2', data=data, headers=headers)
    W = etree.parse(StringIO(W.text))
    root = W.getroot()
    TranslationandAlignmentlist = []
    TranslationArray = []
    AlignmentArray = []
    for element in root.iter():
        if element.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}TranslatedText':
            translations = element.text
            TranslationArray.append(translations)
    for element in root.iter():
        if element.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}Alignment':
            if element.text == None:
                AlignmentArray.append('No Alignment Data')
            else:
                translations = element.text
                AlignmentArray.append(translations)
    #[x for x in AlignmentArray if x is not None]

    TranslationandAlignmentlist.append(TranslationArray)
    TranslationandAlignmentlist.append(AlignmentArray)
    print etree.tostring(W, xml_declaration=True, pretty_print=True, encoding='UTF-8')
    Translation = TranslationandAlignmentlist
    return Translation

def mash_em(Source_text, Translated_text, Alignment):
    Source_text_list = Source_text
    #Creates a list of every word in the Source_text, thus maintaining it's index
    Translated_text_list = Translated_text
    #Creates a list of every word in the Translated_text, thus maintaining it's index
    #print Alignment
    #print "This is Alignment"
    Alignment_line = str(Alignment)
    #print Alignment_line
    #print "This is Alignment_line"
    Newindexes = []
    Indexes = Alignment_line.split(' ')

    for a in Indexes:
        a = str(a)
        a = a.split('-')
        Newindexes.append(a)
    # ensure that the alignment data is a string, and then separate the Source Text indexes and the Translation indexes and saves them together as a list within Newindexes
    # Newindexes is a list that nests multiple lists
    Source_list = []
    Translated_list = []
    for i in Newindexes:
        if len(i)>1 and i != 'No Alignment Data':
            Source_list.append(i[0])
        else:
            Source_list.append('No Source Alignment')
       # This takes the only Source Text indexes from Newindexes and appends them the recently created Source_list

    for i in Newindexes:
        if len(i)>1 and i != 'No Alignment Data':
            Translated_list.append(i[1])
        else:
            Translated_list.append('No Translation Alignment')
        # This takes the only Translated Text indexes from Newindexes and appends them the recently created Translated_list

    Source_list_new = []
    Translated_list_new = []

    for i in Source_list:
        if len(i)>1 and i != 'No Source Alignment':
            i = i.split(':')
            SourceString = Source_text_list[int(i[0]):(int(i[1]) + 1)]
            Source_list_new.append(SourceString.capitalize())
	    #First line of the for loop splits the start and end indices of Source text, because the alignment information cannot be interpreted as a string
	    #Second line joins all of the words for the given alignment index, and appends the newly formed string to the recently created Source_list_new
        else:
            Source_list_new.append(Source_text_list[0:])
    for i in Translated_list:
        if len(i)>1 and i != 'No Translation Alignment':
            i = i.split(':')
            TranslatedString = Translated_text_list[int(i[0]):(int(i[1]) + 1)]
            Translated_list_new.append(TranslatedString.capitalize())
	    #First line of the for loop splits the start and end indices of Translated text, because the alignment information cannot be interpreted as a string
	    #Second line joins all of the words for the given alignment index, and appends the newly formed string to the recently created Translated_list_new
        else:
            Translated_list_new.append(Translated_text_list[0:])

    Dict = {}
    Dict = dict(zip(Source_list_new, Translated_list_new))
    #This creates a dictionary of translations with the Source_list_new as the key, and the Translated_text_new as the value
    return Dict

def list_of_three(Dictionary):
    SeparatingSourceandTranslationandFrequency = []
    for key in Dictionary:
        HopefullyFinalList = []
        key1 = key.split(' = ')
	# creates a list called "key1" which contains the Source text in index 0 and Translated text in index 1
        for i in key1:
            HopefullyFinalList.append(i)
	    #Appends the Source text and translated text to index 0 and index 1 (respectively) of the recently created HopefullyFinalList
        HopefullyFinalList.append(Dictionary[key])
	#Appends the value corresponding to key in dictionary (AKA the frequency) to index 2 of HopefullyFinalList
	SeparatingSourceandTranslationandFrequency.append(HopefullyFinalList)
	#Appends the list containing [Source_text, Translated_text, Frequency] to a new list that will be parsed through using a Django Template
    return SeparatingSourceandTranslationandFrequency

def Finalizer(OutsideList):
    HowAboutAnotherList = []
    for i in OutsideList:
        for mini_i in i:
            HowAboutAnotherList.append(mini_i[0] + ' == ' + mini_i[1])
    Freqcount = collections.Counter(HowAboutAnotherList)
    StillMoreLists = []
    for key in Freqcount:
        GettingCloser = []
        Temporarylist = []
        Temporarylist.append(key.split(' == '))
        Temporarylist.append(Freqcount[key])
        for i in Temporarylist[0]:
            GettingCloser.append(i)
        GettingCloser.append(Temporarylist[1])
        StillMoreLists.append(GettingCloser)
    return StillMoreLists

def useless_dictionary(Dictionary):
    J = '___'.join(['%s = %s' % (key, value) for (key, value) in Dictionary.iteritems()])    
    # Joins all of the Source text with it's corresponding translation. Entries are separated with '___' (three underscores)
    NewJ = []
    NewJ = J.split('___')
    #The entries are separated by their underscores and saved to a recently created list named 'NewJ'

    counter=collections.Counter(NewJ)
    #collections.Counter counts occurrences of an instance in a list
    print counter
    Emptydict = {}
    for k,v in sorted(counter.items()):
	#The Dictionary that resulted from counting 'NewJ' is sorted, and iterated through
        k = k.encode('UTF-8')
        Emptydict[str(k)] = int(v)
	#Fills Emptydict with the string 'Source_text = Translated_text' as the key, and the corresponding frequency as the value
    return Emptydict

def words_from_line(line):
    line = line.decode('UTF-8')
    line = (line.rstrip('\n'))
    #return re.split('(?:\s|[*\r,.:#@()+=<>$;"?!|\[\]^%&~{}«»–])+', line)
    #return re.split('[^a-zA-ZäöëüßÄËÖÜß]+', line)
    return re.compile("(?!['_])(?:\W)+", flags=re.UNICODE).split(line)


def _demo_show_text( text ):
    lines = text.splitlines()
    blocks = []
    this_lines = []
    for line in lines:
        if line == '':
            if this_lines != []:
                blocks.append( '\n'.join( this_lines ) )
                this_lines = []
        else:
            this_lines.append( line )
    if this_lines != []:
        blocks.append( ''.join( this_lines ) )
    normalizer = Normalizer('en')
    res = []
    for b in blocks:
        pattern = re.compile(r'\b([a-zA-Z]+)\b')
        res.append( re.sub(pattern, lambda x: _demo_show_normalized( normalizer, x.group(1) ), b) )
    Final = "\n".join( x+"\n" for x in res )
    return render_to_response('Demo_text.html', {'Final': Final})

def converted(request, doc_id):
    filename = os.path.join(settings.PATH_TO_CONVERTED, doc_id, 'text')
    if '/' in doc_id or not os.path.exists(filename):
        filename = '/dev/null'
    f = filename
    return f

def sentences_in_f(textfile):
    lines = [line.strip() for line in open('textfile')]
    Text_list = start.splitlines(True)
    #print Text_list
    return Text_list


"""
def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value):
                yield subvalue
    else:
        yield o

##########################################
#Working Mash-em#
#########################################
def mash_em(Source_text, Translated_text, Alignment):
    Source_text_list = words_from_line(Source_text)
    #Creates a list of every word in the Source_text, thus maintaining it's index
    Translated_text_list = words_from_line(Translated_text)
    #Creates a list of every word in the Translated_text, thus maintaining it's index
    Newindexes = []
    Indexes = Alignment.split(', ')

    for a in Indexes:
        a = str(a)
        a = a.split('-')
        Newindexes.append(a)
    # ensure that the alignment data is a string, and then separate the Source Text indexes and the Translation indexes and saves them together as a list within Newindexes
    # Newindexes is a list that nests multiple lists
    Source_list = []
    Translated_list = []

    for i in Newindexes:
        Source_list.append(i[0])
    # This takes the only Source Text indexes from Newindexes and appends them the recently created Source_list

    for i in Newindexes:
        Translated_list.append(i[1])
    # This takes the only Translated Text indexes from Newindexes and appends them the recently created Translated_list
    
    Source_list_new = []
    Translated_list_new = []

    for i in Source_list:
        i = i.split(':')
        Source_list_new.append(' '.join(Source_text_list[int(i[0]):(int(i[1]) + 1)]))
	#First line of the for loop splits the start and end indices of Source text, because the alignment information cannot be interpreted as a string
	#Second line joins all of the words for the given alignment index, and appends the newly formed string to the recently created Source_list_new

    for i in Translated_list:
        i = i.split(':')
        Translated_list_new.append(' '.join(Translated_text_list[int(i[0]):(int(i[1]) + 1)]))
	#First line of the for loop splits the start and end indices of Translated text, because the alignment information cannot be interpreted as a string
	#Second line joins all of the words for the given alignment index, and appends the newly formed string to the recently created Translated_list_new
    
    Dict = {}

    Dict = dict(zip(Source_list_new, Translated_list_new))
    #This creates a dictionary of translations with the Source_list_new as the key, and the Translated_text_new as the value
    return Dict



###################################
#Old Notes#
###################################

######################################
#In Case Function Breaks#
######################################
def Frequency_list(request):
    Source_text_test = 'Once upon a time there was a hare who was boasting how he could run faster than anyone.'
    Translated_text_test = 'Einmal gab es einen Hasen der Prahlerei war wie er schneller als jeder andere laufen könnte.'
    Alignment_test = '0:3-0:0, 4:5-1:1, 6:6-3:3, 7:7-4:4, 8:8-5:5, 9:9-7:7, 10:10-6:6, 11:11-8:8, 12:12-9:9, 13:13-15:15, 14:14-14:14, 15:15-10:10, 16:16-11:11, 17:17-12:13'
    Source_text_one = 'Let me.make something very very clear: I like questions? Do you agree that they are awesome! Yeah; you do'
    Source_text_list = words_from_line(Source_text_test)
    Translated_text_list = words_from_line(Translated_text_test)

    Newindexes = []
    Indexes = Alignment_test.split(', ')

    for a in Indexes:
        a = str(a)
        a = a.split('-')
        Newindexes.append(a)

    Source_list = []
    Translated_list = []

    for i in Newindexes:
        Source_list.append(i[0])

    for i in Newindexes:
        Translated_list.append(i[1])

    Source_list_new = []
    Translated_list_new = []

    for i in Source_list:
        i = i.split(':')
        Source_list_new.append(' '.join(Source_text_list[int(i[0]):(int(i[1]) + 1)]))


    for i in Translated_list:
        i = i.split(':')
        Translated_list_new.append(' '.join(Translated_text_list[int(i[0]):(int(i[1]) + 1)]))

    Dict = {}

    Dict = dict(zip(Source_list_new, Translated_list_new))
    #print Dict
    #print "\nThe above is the output of 'Dict'\n"
    print 'Here is your Frequency List:'
    for key, value in Dict.iteritems():
        print key + ((30 - int(len(str(key)))) * ' ') + value
    # I need to add the frequency of each Source, Translation pair, and remove any duplicates
    # The best way to do this is to first find the frequency of each pair
    #Dict = collections.Counter(Dict)
    #print Dict
    Dictionary = Dict
    Emptydict = {}
    J = '___'.join(['%s = %s' % (key, value) for (key, value) in Dictionary.iteritems()])    
    #print J
    #print "\nThe above is the output of 'J'\n"
    NewJ = []
    NewJ = J.split('___')
    #print NewJ
    #print "\nThe above is the output of 'NewJ'\n"
    counter=collections.Counter(NewJ)
    #print counter
    #print "\nThe above is the output of 'counter'\n"
    FrequencylistDictionary = {}
    for k,v in sorted(counter.items()):
        NewestList = []
        k = k.encode('UTF-8')
        #print k
        #print "\nThe above is the output of 'k'\n"
        Final = ('{}: {}'.format(k,v))
        Emptydict[str(k)] = int(v)
        #print Emptydict
        #print "\nThe above is the current output of 'Emptydict'\n"
    SeparatingSourceandTranslationandFrequency = []
    #Should be a list of lists
    for key in Emptydict:
        HopefullyFinalList = []
        #print key
        #print 'This is the key in Emptydict'
        key1 = key.split(' = ')
        for i in key1:
            HopefullyFinalList.append(i)
        HopefullyFinalList.append(Emptydict[key])
	SeparatingSourceandTranslationandFrequency.append(HopefullyFinalList)
	TemplateList = SeparatingSourceandTranslationandFrequency
	
        #print HopefullyFinalList
    return render_to_response('Frequency_list.html', {'TemplateList': TemplateList})

########################################################################################


allowed_symbols = {
    'de':   u'^[a-zäöüA-ZÄÖÜß]*$',
}
def get_words(lines, group_by=[1], language=None):

    #Returns hash of words in a file
    #word => number

    language_filter = allowed_symbols.get(language)
    result = {}
    (a, b, c) = ("", "", "")
    for line in lines:
        words = words_from_line(line)
        for word in words:
            if re.match('[0-9]*$', word):
                continue
            if language_filter and not re.match(language_filter, word):
                continue
            result.setdefault(word, 0)
            result[word] += 1
            if 2 in group_by and a != "" and b != "":
                w = "%s_%s" % (a,b)
                result.setdefault(w, 0)
                result[w] += 1
            if 3 in group_by and not "" in [a,b,c]:
                w = "%s_%s_%s" % (a,b,c)
                result.setdefault(w, 0)
                result[w] += 1
            (a,b,c) = (b, c, word)

    #logging.debug(result)
    return result
print words_from_line(Source_text_one)

######
"""
