from PIL import Image
from pytesseract import pytesseract
from bs4 import BeautifulSoup
import requests
import pandas as pd

response = requests.get("https://www.iana.org/help/example-domains")
doc = BeautifulSoup(response.text, "html.parser")

img = doc.find("img")
alternative_text = img["alt"] if img else "Imagem não encontrada"
print("Texto alternativo da imagem:", alternative_text)

with open("saida.txt", "w", encoding="utf-8") as f:
    f.write(alternative_text)