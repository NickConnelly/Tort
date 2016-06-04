from base import GetEndpoint, CONTENT, LANGUAGE_CODES
import json
import requests
import datetime
import math
#import retry
import time
import urllib
import urllib2
import xml.etree.cElementTree as ET
import xml.dom.minidom

class TranslateEndpoint(GetEndpoint):
    endpoint = 'Translate'

    def __init__(self, text, to, tfrom=''):

        if tfrom and tfrom not in LANGUAGE_CODES or to not in LANGUAGE_CODES:
            raise ValueError('Invalid language codes')

        self.convert_kwargs(locals())

    def process_response(self, resp):
        root = self.parse_xml(resp)
        return root.text

class TranslateArrayEndpoint(GetEndpoint):
    endpoint = 'TranslateArray2'

    def __init__(self, text, to, tfrom=''):

        if tfrom and tfrom not in LANGUAGE_CODES or to not in LANGUAGE_CODES:
            raise ValueError('Invalid language codes')

        self.convert_kwargs(locals())

    def process_response(self, resp):
	resp = str(resp)
	print resp
    print "Looking for the problem 2"

	#for i in resp:
	#    print i
	#root = self.parse_xml(resp)
	#return root.text


