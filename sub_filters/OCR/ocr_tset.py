from PIL import Image
import pytesseract

print(pytesseract.image_to_string(Image.open('sub_filters/OCR/phone-number.png')))