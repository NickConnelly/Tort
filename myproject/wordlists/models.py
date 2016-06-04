# -*- coding: utf-8 -*-

import os
import sys
from time import strftime
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

from colorful.fields import RGBColorField

from binascii import hexlify

def _createId():
    return hexlify(os.urandom(16))

class WordList(models.Model):
    list_id = models.CharField(max_length=32, primary_key=True, default=_createId)
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, editable=False)
    language = models.CharField(max_length=50, null=True, choices=settings.VALID_LANGUAGES)
    description = models.CharField(max_length=5000, null=True)
    primary = models.BooleanField(default=False)
    color = RGBColorField()

    def __unicode__(self):
        return self.title

    def _known_words_filename(self):
        if self.primary:
            wordlist_file = "main"
        else:
            wordlist_file = self.list_id

        return os.path.join(settings.PATH_TO_WORDLISTS, self.user.username, self.language, wordlist_file)

    def load_words(self):

        f = self._known_words_filename()
        if os.path.exists(f):
            words = [ x.strip() for x in open(f).read().splitlines() ]
            return [ x for x in words if x != "" ]
        else:
            return []

    def has_word(self, words):
        my_words = self.load_words()
        return all( w in my_words for w in words )

    def save_words(self, saved_words):

        f = self._known_words_filename()
        if not os.path.exists(f):
            f_dir, _ = os.path.split(f)
            if not os.path.exists(f_dir):
                os.makedirs(f_dir)

        existent_words = self.load_words()
        words = [ x.strip() for x in saved_words if x.strip() not in existent_words ]

        words_utf8 = []
        for w in words:
            try:
                words_utf8.append( w.encode('utf8') )
            except:
                print "Can not convert word to unicode: %s" % w

        try:
            open(f, "a").write("\n".join(words_utf8)+"\n")
            return True
        except Exception, e:
            print e
            return False

    def grouped_words(self):
        """
        Return three dictionaries:
        * dictionary of words in the wordlists gropued by normalized word.
        * part-of-speech tags for each word
        * short translation for each word
        """

        sys.path.append( settings.PATH_TO_NEW_WORDS )
        from mystemmer import Normalizer
        normalizer = Normalizer(self.language)

        words = self.load_words()
        result = {}
        tags = {}
        translation = {}

        for w in words:
            n = normalizer.normalize(w)
            if n in result:
                result[n].append( w )
            else:
                result[n] = [ w ]
            
            this_translation = normalizer.translate( w )
            if this_translation:
                translation[n] = this_translation

            this_tags = normalizer.tags( w )
            if this_tags:
                tags[n] = this_tags

        return result, tags, translation


    def delete(self):

        try:
            f = self._known_words_filename()
        except:
            return False

        try:
            os.remove(f)
            return True
        except:
            return False

    def merge(self, wl):
        return self.save_words( wl.load_words() )
