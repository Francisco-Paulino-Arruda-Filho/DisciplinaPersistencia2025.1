from bs4 import BeautifulSoup
import requests

response = requests.get("https://example.com/")
doc = BeautifulSoup(response.text, "html.parser")

title = doc.title.string
links = doc.select("a[href]")    

print("Título da página:", title)
print("Textos dos links encontrados:")

for link in links:
    texto = link.text.strip()
    if texto:  
        print(f"- {texto}")

response_2 = requests.get("https://www.iana.org/help/example-domains")
doc_2 = BeautifulSoup(response_2.text, "html.parser")

title_2 = doc_2.title.string
links_2 = doc_2.select("a[href]")

for link in links_2:
    texto = link.text.strip()
    if texto:  
        print(f"- {texto}")