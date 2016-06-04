# -*- coding: utf-8 -*-

import re
import collections
from django.shortcuts import render_to_response
from Frequency_list_functions import words_from_line, mash_em, useless_dictionary, list_of_three, converted, sentences_in_f, Create_xml, maketranslate, docsplitter, Finalizer
import nltk
import collections


def Frequency_list(request, doc_id):
    print doc_id
    SourceTextArray = docsplitter('myproject/converted/' + str(doc_id) + '/text')
    #Split the text in doc_id into a list of sentences
    TranslationandAlignmentlist = maketranslate(SourceTextArray)
    #maketranslate returns a list of list. The first list is the translations, the second list is the alignments.
    TranslatedTextArray = TranslationandAlignmentlist[0]
    AlignmentArray = TranslationandAlignmentlist[1]
    OutsideList = []
    count = 0
    for i in SourceTextArray:
        Source_text_test = SourceTextArray[count]
        Translated_text_test = TranslatedTextArray[count]
        Alignment_test = AlignmentArray[count]
        count += 1
        Dict = mash_em(Source_text=Source_text_test, Translated_text=Translated_text_test, Alignment=Alignment_test)
        #mash_em uses the translation alignment to return a dictionary where the key is the Source Text, and the value is the Translation.
        """print 'Here is your Frequency List:'
        for key, value in Dict.iteritems():
            key = key.encode('utf-8')
            #key = unicode(key, 'utf-8', errors='replace')
            value = value.encode('utf-8')
            #value = unicode(value, 'utf-8', errors='replace')
            print key + ((30 - int(len(str(key)))) * ' ') + value"""
        #The comment above is used for command line debugging
        Emptydict = useless_dictionary(Dict)
        List_of_three_result = list_of_three(Emptydict)
        OutsideList.append(List_of_three_result)
    TemplateList = Finalizer(OutsideList)
    # next step is to get rid of all capitals, match up the identical matches, create the cummulative frequencies, and CamelCase the source and translations
    # Then, find a way to remove ")" and "?" from sentences.
    # Then, find very common matches, like "?" and "." and ")" and remove them from the list.
    return render_to_response('Frequency_list.html', {'TemplateList': TemplateList})
        #return render_to_response('mark-frequency-list.html', {'TemplateList': TemplateList})
# Still need to make it look cleaner, and get rid of punctuation, and get rid of words connected to punctuation.

"""
################################################
#Working Version#
###############################################

def Frequency_list(request, doc_id):
    #Start by splitting doc_id into the sentences that comprise it
    #Add those sentences into a list that can be sent into maketranslate
    #capture the output and save it to two seperate lists using [0] and [1]
    #Make this function one big for loop, going through the indexes of the lists
    Source_text_test = 'Once upon a time there was a hare who was boasting how he could run faster than anyone.'
    Translated_text_test = 'Einmal gab es einen Hasen der Prahlerei war wie er schneller als jeder andere laufen könnte.'
    Alignment_test = '0:3-0:0, 4:5-1:1, 6:6-3:3, 7:7-4:4, 8:8-5:5, 9:9-7:7, 10:10-6:6, 11:11-8:8, 12:12-9:9, 13:13-15:15, 14:14-14:14, 15:15-10:10, 16:16-11:11, 17:17-12:13'
    Dict = mash_em(Source_text=Source_text_test, Translated_text=Translated_text_test, Alignment=Alignment_test)
    ###Command Line Confirmation for debugging
    print 'Here is your Frequency List:'
    for key, value in Dict.iteritems():
        print key + ((30 - int(len(str(key)))) * ' ') + value
    ###Command Line Confirmation for debugging
    Emptydict = useless_dictionary(Dict)
    TemplateList = list_of_three(Emptydict)
    return render_to_response('Frequency_list.html', {'TemplateList': TemplateList})
    #return render_to_response('mark-frequency-list.html', {'TemplateList': TemplateList})

###################

def Frequency_list(request, doc_id):
    source_array = converted(request, doc_id)
    source_array = sentences_in_f(f)
    # source_array should be an array of source text sentences
    # source_array is what should be sent to Microsoft, and the resulting translations will be saved as translated_array
    # The translation alignments would be saved as allignment_array
    # We would then need to iterate through the arrays, starting at index 0, and adding one each loop.
    # the given index data would be saved as Source_text, Translated_text, and Alignment
    Source_text_test = 'Once upon a time there was a hare who was boasting how he could run faster than anyone.'
    Translated_text_test = 'Einmal gab es einen Hasen der Prahlerei war wie er schneller als jeder andere laufen könnte.'
    Alignment_test = '0:3-0:0, 4:5-1:1, 6:6-3:3, 7:7-4:4, 8:8-5:5, 9:9-7:7, 10:10-6:6, 11:11-8:8, 12:12-9:9, 13:13-15:15, 14:14-14:14, 15:15-10:10, 16:16-11:11, 17:17-12:13'
    Dict = mash_em(Source_text=Source_text_test, Translated_text=Translated_text_test, Alignment=Alignment_test)
    ###Command Line Confirmation for debugging
    print 'Here is your Frequency List:'
    for key, value in Dict.iteritems():
        print key + ((30 - int(len(str(key)))) * ' ') + value
    ###Command Line Confirmation for debugging
    Emptydict = useless_dictionary(Dict)
    TemplateList = list_of_three(Emptydict)

    return render_to_response('Frequency_list.html', {'TemplateList': TemplateList})


# I need to Get_text_file from the document that I am working with. Then I need to break that text file into an array of sentences.
#Then send that array to Microsoft to be translated. Source, Translation, and alignment all need to be saved as doc.id values that can be called.
#Receive those translations and alignments and call them inside of Frequency_list.
Priorities:
1. Obviously figure out how to pull the frequency list inputs from Microsoft
2. Add the "Frequency_list" template as an option on the document/uploaded assets page
-------<a href="{{ url "Frequency_list" document.doc_id %}" class="list-group-item-text">Frequency List</a>
3. Give "Frequency_List" The formating from "Wordlists" 
4. Give "Fequency_list" the same "Save_word" functionality
5. Figure out how to host this app for free on the internet
6. Figure out how to apply the code to an array of sentences, or even 50 sentences
7. Figure out how to do a character count on a document before it is sent to Microsoft
"""
