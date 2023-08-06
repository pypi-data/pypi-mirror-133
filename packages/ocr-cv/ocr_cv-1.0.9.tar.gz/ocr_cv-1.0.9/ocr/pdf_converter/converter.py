import pytesseract
from pdf2image import convert_from_bytes

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Convert PDF file bytes to string


class PdfConverter:
    def __init__(self, file_bytes: bytes):
        self.bytes = file_bytes

    def convert(self) -> str:
        pages = convert_from_bytes(self.bytes)

        text = ''

        for page in pages:
            text += pytesseract.image_to_string(page)

        return text
