from os import path

from src.main import get_keywords

dir_path = path.dirname(path.realpath(__file__))
filename = path.join(dir_path, '../ocr/mock/Gal-Ben-Haim-CV.pdf')
file_bytes: bytes = open(filename, 'rb').read()

keywords = get_keywords(file_bytes)

print(keywords)
