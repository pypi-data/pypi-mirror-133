from keywords.locator import KeyWordsLocator
from pdf_converter.converter import PdfConverter

# Returns a filtered dictionary by keywords found in a PDF file
# First we convert the file to string
# Then we filter the given default_categories dictionary by keywords found in the files content


def get_keywords(file_bytes: bytes, categories: dict[str, list[str]]) -> dict[str, list[str]]:
    text: str = PdfConverter(file_bytes).convert()
    return KeyWordsLocator(text, categories).get_keywords()
