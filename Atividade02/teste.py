from PIL import Image
from pytesseract import pytesseract
from bs4 import BeautifulSoup
import requests
import os

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
doc = BeautifulSoup(response.text, "html.parser")

img = doc.find("img")
alternative_text = img["alt"] if img else "Imagem não encontrada"

with open("saida.txt", "w", encoding="utf-8") as f:
    f.write(alternative_text)

if img and img.get("src"):
    img_src = img["src"]

    base_url = "http://books.toscrape.com/"
    img_url = os.path.join(base_url, img_src.replace("../", ""))

    img_response = requests.get(img_url)
    if img_response.status_code == 200:
        with open("livro.jpg", "wb") as f:
            f.write(img_response.content)

        img = Image.open("livro.jpg")
        text = pytesseract.image_to_string(img)


        with open("texto_ocr.txt", "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print("Erro ao baixar a imagem:", img_response.status_code)
else:
    print("Imagem não encontrada ou sem atributo 'src'")
