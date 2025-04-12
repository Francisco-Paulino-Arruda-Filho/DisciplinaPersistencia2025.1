from bs4 import BeautifulSoup
import requests

response = requests.get("https://quotes.toscrape.com/")

doc = BeautifulSoup(response.text, "html.parser")
title = doc.title.string
print(title)

text = doc.select_one("span.text").text
print(text)
author = doc.select_one("small.author").text
print(author)