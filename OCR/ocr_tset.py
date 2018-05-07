from PIL import Image
import pytesseract

print(pytesseract.image_to_string(Image.open('OCR/firefox_2017-10-29_02-07-54.png')))
