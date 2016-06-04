
# vim: encoding: utf-8

import sys
import os
import re
import Stemmer

LINGUISTIC_DATA_DIR = os.path.join( os.path.dirname(__file__), 'linguistic-data' )
linguistic_data = {
    'en':   {
        'stemmer':                  'english',
        'words_file':               'en-words.txt',
        'verbs_file':               'en-verbs.txt',
        'irregular_verbs_file':     'en-irregular-verbs.txt',
        'irregular_plurals_file':   'en-irregular-plurals.txt',
        'tags_file':                'en-tags.txt',
        'short_file':               'en-ru-short.txt',
    },
    'de' : {
        'stemmer':                  'german',
    },
    'fr' : {
        'stemmer':                  'french',
    },
    'es' : {
        'stemmer':                  'spanish',
    },
    'it' : {
        'stemmer':                  'italian',
    },
    'ru' : {
        'stemmer':                  'russian',
    },
    'uk' : {
        'stemmer':                  'ukrainian',
    }
}

ENGLISH_CONSONANTS = "bcdfghjklmnpqrstvwxz"

language = 'en'

def _common_part(a, b):
    """
    Try to find the longest common part between a and b (from the beginning).
    Case of a can be changed to find the longest part.
    Case of b is not changed and stays as it is.
    """

    # case sensitive
    common = ""
    for i in range(len(a)):
        if i >= len(b):
            break
        if a[i] != b[i]:
            break
        common = a[:i+1]
    common_case_sensitive = common

    # case insensitive
    a = a.lower()

    common = ""
    for i in range(len(a)):
        if i >= len(b):
            break
        if a[i] != b[i]:
            break
        common = a[:i+1]
    common_case_insensitive = common

    if len(common_case_sensitive) == len(common_case_insensitive):
        return common_case_sensitive
    else:
        return common_case_insensitive


class Normalizer(object):

    def __new__(cls, *args, **kwargs):
        if cls is Normalizer:                             # <-- required because NormalizerEnglish's
            #language, args = args[0], args[1:]              #     __new__ method is the
            if args[0] == 'en':                            #     same as Normalizer's
                instance = NormalizerEnglish(*args, **kwargs);
            elif args[0] == 'de':
                instance = NormalizerGerman(*args, **kwargs);
            elif args[0] == 'fr':
                instance = NormalizerFrench(*args, **kwargs);
            elif args[0] == 'es':
                instance = NormalizerSpanish(*args, **kwargs);
        else:
            instance = super(Normalizer, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, language, stem_unknown=True):
        self.lang_data = linguistic_data[language]
        self.stemmer = Stemmer.Stemmer( self.lang_data['stemmer'] )

        self.lang_verbs = set(self._load_words( 'verbs' ))
        self.lang_irregular_verbs = self._load_declinated_words( 'irregular_verbs' )
        self.lang_irregular_plurals = self._load_declinated_words( 'irregular_plurals' )
        self.lang_tags = self._load_dict( 'tags' )
        self.lang_short_translation = self._load_dict( 'short' )

        self.stem_unknown = stem_unknown
        self.full_word = self._load_stemmed()

    def _load_words(self, file_type):
        try:
            f = self.lang_data[ file_type + "_file" ]
        except:
            return []

        f = os.path.join( LINGUISTIC_DATA_DIR, f )

        if not os.path.exists( f ):
            return []

        return [ w.strip() for w in open(f).readlines() ]

    def _load_dict(self, file_type):

        result = {}
        try:
            f = self.lang_data[ file_type + "_file" ]
        except:
            return result

        f = os.path.join( LINGUISTIC_DATA_DIR, f )

        if not os.path.exists( f ):
            return result

        for w in open(f).readlines():
            w = w.strip().decode('utf8')
            if ' ' in w:
                k, v = w.split(' ', 1)
                result[k] = v

        return result

    def _load_declinated_words(self, file_type):

        try:
            f = self.lang_data[ file_type + "_file" ]
        except:
            return {}

        f = os.path.join( LINGUISTIC_DATA_DIR, f )

        if not os.path.exists( f ):
            return {}

        res = {}
        for line in open(f).readlines():
            if line.startswith('#'):
                continue
            line = line.strip().lower()
            words = line.split()
            for w in words[1:]:
                if '/' in w:
                    declinated_words = w.split('/')
                else:
                    declinated_words = [ w ]
                for dw in declinated_words:
                    res[ dw.lower() ] = words[0].lower()
        return res

    def _load_stemmed(self):
        full_word = {}

        f = self.lang_data.get("words_file")
        if not f:
            return {}
        f = os.path.join( LINGUISTIC_DATA_DIR, f )
        if not os.path.exists(f):
            return {}

        for word in open(f).readlines():
            word = word.strip()
            stemmed = self.stem(word)
            if stemmed in full_word:
                full_word[stemmed].append( word ) 
            else:
                full_word[stemmed] = [ word ]

        return full_word


    def is_verb(self, w):
        return w.lower() in self.lang_verbs

    def irregular_verb(self, w):
        """
        Returns base form of the word
        or None is w is not a irregular verb.
        """
        return self.lang_irregular_verbs.get( w.lower() )

    def irregular_plural(self, w):
        return self.lang_irregular_plurals.get( w.lower() )

    def _choose_best_word(self, word, word_options):
        raise NotImplementedError

    def stem(self, word):
        return self.stemmer.stemWord(word.lower())

    def translate(self, word):
        return self.lang_short_translation.get(word, '')

    def tags(self, word):
        return self.lang_tags.get(word, '')

    def normalize(self, word):

        normalized_irregular_verb = self.irregular_verb( word )
        normalized_irregular_plural = self.irregular_plural( word )

        if  normalized_irregular_verb and word != normalized_irregular_verb:
            return normalized_irregular_verb

        if  normalized_irregular_plural and word != normalized_irregular_plural:
            return normalized_irregular_plural

        stemmed = self.stem( word )
        word_options = self.full_word.get(stemmed, [])

        if word_options == []:
            if word.endswith('est'):
                return self.normalize(word[:-3])

        if word_options == []:
            if self.stem_unknown:
                return stemmed
            else:
                return '?'
        else:
            return self._choose_best_word( word, word_options )

class NormalizerEnglish(Normalizer):

    def _choose_best_word(self, word, word_options):
        # CAUTION: English specific

        if word in word_options:
            return word

        # handling special cases:
        #   * verb endings
        #   * plurals

        if word.lower() in ['ed', 'ing', 'ies']:
            return word

        # handling verb tenses
        # http://www.oxforddictionaries.com/words/verb-tenses-adding-ed-and-ing
        if word.endswith('ed') or word.endswith('ing'):

            if word.endswith('ed'):
                word = word[:-2]
            else:
                word = word[:-3]

            if self.is_verb(word + 'e'):
                word = word + 'e'

            if len(word) > 1 and word[-1] == word[-2] and word[-1] in ENGLISH_CONSONANTS:
                word = word[:-1]

        # handling irregular plurals
        # http://web2.uvcs.uvic.ca/elc/studyzone/330/grammar/irrplu.htm
        elif word.endswith('ies'):
            word = word[:-3]+'y'
        elif word.endswith('oes'):
            word = word[:-3]+'o'

        common = {}
        for w in word_options:
            c = _common_part(word, w)
            if c in common:
                common[c].append(w)
            else:
                common[c] = [w]

        best_options = [ common[k] for k in sorted( common.keys(), key=lambda x:-len(x) )][0]
        best_answer = sorted( best_options, key=lambda x:len(x) )[0]
        
        return best_answer

NormalizerGerman = NormalizerEnglish
NormalizerFrench = NormalizerEnglish
NormalizerSpanish = NormalizerEnglish


def _demo_show_normalized(normalizer, word):
    normalized = normalizer.normalize(word)
    if normalized != word:
        return "%s(%s)" % (word, normalized)
    else:
        return word

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

    return "\n".join( x+"\n" for x in res )

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print """
Usage:
    
    %s  --normalize LANG WORD

Show normalized WORD.

    %s  FILES...

Normalize words in texts in FILES and show normal form of words near original words in the texts.
"""
    else:
        if sys.argv[1] == '--normalize':
            language == sys.argv[2]
            word = sys.argv[3]

            if language != 'en':
                print word
            else:
                normalizer = Normalizer(language)
                print normalizer.normalize( word )

        else:
            for f in sys.argv[1:]:
                print _demo_show_text( file(f).read() )

