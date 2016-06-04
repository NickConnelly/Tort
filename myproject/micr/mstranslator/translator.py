from mstranslator import MStranslator
from django.conf import settings


def maketranslate(self):
    key = settings.MS_TRANSLATOR_KEY
    translator = MSTranslator(key)
    Translation = translator.translate(text='This is a lot of work for nothing', tfrom='en', to='de')
    return render_to_response('translate.html', {'translation_here': Translation})

"""
client = MicrosoftTranslatorClient('client_id', 'client_secret')
Translation = client.TranslateText('Hello Jessica, this is what I have been working on', 'en', 'fr')
return render_to_response('translate.html', {'translation_here': Translation})
"""
