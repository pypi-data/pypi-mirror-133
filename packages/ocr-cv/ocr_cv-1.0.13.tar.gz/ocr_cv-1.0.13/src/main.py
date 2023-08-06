from ocr.keywords.locator import KeyWordsLocator
from ocr.keywords.defaults import default_categories
from ocr.pdf_converter.converter import PdfConverter

# Returns a filtered dictionary by keywords found in a PDF file
# First we convert the file to string
# Then we filter the given default_categories dictionary by keywords found in the files content


def get_keywords(file_bytes: bytes, categories=default_categories) -> dict[str, list[str]]:
    text: str = PdfConverter(file_bytes).convert()
    return KeyWordsLocator(text, categories).get_keywords()
