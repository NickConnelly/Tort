from myproject.micr.Translator.TranslateAPI import MicrosoftTranslatorClient
from django.shortcuts import render_to_response



def maketranslate(self):
	client = MicrosoftTranslatorClient('client_id', 'client_secret')
	Translation = client.TranslateText('Hello Jessica, this is what I have been working on', 'en', 'fr')
	return render_to_response('translate.html', {'translation_here': Translation})

