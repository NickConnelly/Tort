from base import GetEndpoint, CONTENT, LANGUAGE_CODES

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

    def __init__(self, text, to, tfrom=''):

        if tfrom and tfrom not in LANGUAGE_CODES or to not in LANGUAGE_CODES:
            raise ValueError('Invalid language codes')

        self.convert_kwargs(locals())

    def process_response(self, resp):
        root = self.parse_xml(resp)
        return root.text
