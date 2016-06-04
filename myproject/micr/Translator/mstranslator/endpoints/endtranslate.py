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
    endpoint = 'TranslateArray'
    def __init__(self, texts, to):


        self.convert_kwargs(locals())

    def process_response(self, resp):
        root = self.parse_xml(resp)
        return root.text
    print "Looking for the problem 3"

"""
class TranslateArrayEndpoint(GetEndpoint):
    endpoint = 'Translate'

    def __init__(self, text, to, tfrom=''):

        if tfrom and tfrom not in LANGUAGE_CODES or to not in LANGUAGE_CODES:
            raise ValueError('Invalid language codes')

        self.convert_kwargs(locals())

    def process_response(self, resp):
        root = self.parse_xml(resp)
	print resp
	print root
	print root.text
        return root.text
"""

