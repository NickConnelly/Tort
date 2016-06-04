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


client_id = '263ee1af-8087-4592-bf85-5941238bdab6'
client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='
MS_TRANSLATOR_KEY = MSTranslatorAccessKey(client_id, client_secret)
key = MS_TRANSLATOR_KEY

"""
def maketranslate(self):
    key = MS_TRANSLATOR_KEY
    translator = MSTranslator(key)
    msarray = ['I love scotch', 'How now brown cow', 'We are the knights who say "Ni"']
    Translation = translator.translate(text=raw_input('Type what you want to translate here: '), tfrom='en', to='de')
    
    return render_to_response('translate.html', {'translation_here': Translation})
"""

def Create_xml(Array, from_language, to_language):
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
        string.text = str(i)
    To = etree.SubElement(root, 'To')
    To.text = str(to_language)
    s = etree.tostring(root, xml_declaration=True, pretty_print=True, encoding='UTF-8')
    print "The above is the Output of the Create_xml function"
    return s


def maketranslate(self):
    translator = MSTranslator(key)
    msarray = ['Hey Jessica, I cannot seem to understand why there are so many errors with the Microsoft Translator Alignment data.', 'Oh goodness Jessica, you look beautiful.', 'I guess you dont realize how beautiful you are.']
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
            print "All Done!"
    for element in root.iter():
        if element.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}Alignment':
            translations = element.text
            AlignmentArray.append(translations)
            print "All Done!"
    print TranslationArray
    print AlignmentArray
    TranslationandAlignmentlist.append(TranslationArray)
    TranslationandAlignmentlist.append(AlignmentArray)
    print TranslationandAlignmentlist
    print etree.tostring(W, xml_declaration=True, pretty_print=True, encoding='UTF-8')
    Translation = TranslationandAlignmentlist
    return render_to_response('translate.html', {'translation_here': Translation})

# The next step is to have maketranslate() accept an array as an input, and to have that array be the array sent to Create_XML
# That way I can call the function on the array, and also use it on the next step (merging all of the source, translations, and alignment)
# Save the XML to a file, and then upload that file rather than returning a string value
    #print W.status_code
    #print W.headers
    #print W.encoding
    #print W.text
    #print W.raw
"""
#########################################################
#Perfectly Functioning MakeTranslate#
#########################################################

def maketranslate(self):
    translator = MSTranslator(key)
    headers = {'Authorization': translator.get_authorization_string(), 'content-type': 'application/xml'}
    msarray = ['Hey Jessica, I cannot seem to understand why there are so many errors with the Microsoft Translator Alignment data.', 'Oh goodness Jessica, you look beautiful.', 'I guess you dont realize how beautiful you are.']
    XML_Doc = Create_xml(Array=msarray, from_language = 'en', to_language = 'de')
    print XML_Doc
    data = XML_Doc
    W = requests.post(url='http://api.microsofttranslator.com/V2/Http.svc/TranslateArray2', data=data, headers=headers)
    W = etree.parse(StringIO(W.text))
    root = W.getroot()
    TranslationArray = []
    AlignmentArray = []
    for element in root.iter():
        if element.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}TranslatedText':
            translations = element.text
            TranslationArray.append(translations)
            print "All Done!"
    for element in root.iter():
        if element.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}Alignment':
            translations = element.text
            AlignmentArray.append(translations)
            print "All Done!"
    print TranslationArray
    print AlignmentArray
    #print root.findall('./TranslateArrayResponse/TranslatedText')
   
    print etree.tostring(W, xml_declaration=True, pretty_print=True, encoding='UTF-8')
    Translation = TranslationArray
    return render_to_response('translate.html', {'translation_here': Translation})







 for TranslatedText in root.iter('TranslatedText'):
        print "Hello babydoll"
        for TranslatedText in TranslateArrayResponse.findall('TranslatedText'):
        #Translationsa = TranslateArrayResponse.findall('TranslatedText')
            translationsah = TranslatedText.text
            print translationsah
            print "Is that what you wanted?"
    #for child in root:
        #print child
        #print "These are Children"
        #if child.tag == 'TranslatedText':
            #print child.attrib
            #print "These are attributes"
msarray = ['Hey there Jenny, would you like you eat an apple?', 'looking good', 'I guess']

def auth_token_please(self):


        data = urlencode(dict(
            client_id = '263ee1af-8087-4592-bf85-5941238bdab6',
            client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw=',
            grant_type = 'client_credentials',
            scope = 'http://api.microsofttranslator.com'
        ))

        request = Request(url='https://datamarket.accesscontrol.windows.net/v2/OAuth2-13', data=data)
        response = urlopen(request)
        response = json.loads(response.read())

        self.access_key = response['access_token']
        self.expiry = int(response['expires_in'])
        print 'access token is: ' + self.access_key

        return self.access_key



def straightshot(self):

        data = urlencode(dict(
            client_id = '263ee1af-8087-4592-bf85-5941238bdab6',
            client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw=',
            grant_type = 'client_credentials',
            scope = 'http://api.microsofttranslator.com'
        ))

        request = Request(url='https://datamarket.accesscontrol.windows.net/v2/OAuth2-13', data=data)
        response = urlopen(request)
        response = json.loads(response.read())

        self.access_key = response['access_token']
	Access_token = self.access_key
        self.expiry = int(response['expires_in'])
        print 'access token is: ' + self.access_key




	params = {
	'texts': msarray,
	'from': 'en',
	'to': 'de'
	}
	headers = {
	'Authorization': 'Bearer ' + Access_token
        }
	r = requests.post("http://api.microsofttranslator.com/V2/Http.svc/TranslateArray", params=params, headers=headers)
    


client = MicrosoftTranslatorClient('client_id', 'client_secret')
Translation = client.TranslateText('Hello Jessica, this is what I have been working on', 'en', 'fr')
return render_to_response('translate.html', {'translation_here': Translation})
"""
