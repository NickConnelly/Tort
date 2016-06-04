import sys
import os
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

import guess_language

from myproject.assets.models import Document
from django.core.files import File

CONVERTORS_PATH = os.path.dirname(__file__)
NEW_WORDS_PATH = os.path.join(os.path.dirname(__file__), '..', 'new-words', 'new-words')
ORIGINAL_MEDIA_PATH = os.path.join(os.path.dirname(__file__), '..', 'media')
CONVERTED_MEDIA_PATH = os.path.join(os.path.dirname(__file__), '..', 'converted')

ERROR_UNKNOWN_TYPE_OF_FILE = 'Unknown type of file'
ERROR_CONVERSION_ERROR = 'Conversion error'

SUPPORTED_TYPES = [ 'pdf', 'plain', 'html', 'msword' ]

def convertor_path(f_type):
    return os.path.join(CONVERTORS_PATH, f_type)

def type_detector_path():
    return os.path.join(CONVERTORS_PATH, 'get_file_type')

def get_type_of_file(f):
    p = subprocess.Popen([type_detector_path(), f], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        file_type = stdout.strip()
    if file_type not in SUPPORTED_TYPES:
        return None
    else:
        return file_type

def get_txt_path(doc_id):
    return os.path.join(CONVERTED_MEDIA_PATH, doc_id, 'text')


def create_directory_for_converted(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def convert_file_to_txt(f_from, f_to, f_type):
    converted = False
    create_directory_for_converted(f_to)
    print [convertor_path(f_type), f_from, f_to]
    p = subprocess.Popen([convertor_path(f_type), f_from, f_to], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    converted = p.returncode == 0
    if not converted:
        print stdout
    return converted 

def generate_word_list(f_from, language):
    cmd = [sys.executable, NEW_WORDS_PATH, '-l', language, '-g', '-n', '-N', f_from]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    converted = p.returncode == 0
    if converted:
        words_file = os.path.join(os.path.dirname(f_from), 'words')
        open(words_file, "w").write(stdout)
    else:
        print stderr
    return converted


doc_id = sys.argv[1]
docs = Document.objects.filter(doc_id=doc_id)
if len(docs) == 0:
    print "Document %s not found" % doc_id
    sys.exit(1)

doc = docs[0]
asset_path = os.path.join(ORIGINAL_MEDIA_PATH, "%s" % doc.docfile)
txt_path = get_txt_path(doc_id)
type_of_file = get_type_of_file(asset_path)

error_string = ''
if type_of_file:
    converted = convert_file_to_txt(asset_path, txt_path, type_of_file)
    language = guess_language.guessLanguage(file(txt_path).read())
    if not converted:
        error_string = ERROR_CONVERSION_ERROR
    if converted:
        generate_word_list(txt_path, language)
else:
    converted = False
    error_string = ERROR_UNKNOWN_TYPE_OF_FILE

doc.converted = converted
doc.format_type = type_of_file
doc.language = language
doc.size = os.stat(asset_path).st_size
doc.txtfile = txt_path

print 'language =', doc.language

doc.save()

sys.exit(0)



