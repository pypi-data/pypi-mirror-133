from main import get_keywords
from keywords.defaults import default_categories

from os import path


dir_path = path.dirname(path.realpath(__file__))
filename = path.join(dir_path, 'mock/Gal-Ben-Haim-CV.pdf')
file_bytes: bytes = open(filename, 'rb').read()

keywords = get_keywords(file_bytes, default_categories)

print(keywords)
