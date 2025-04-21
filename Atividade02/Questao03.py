import mimetypes
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def process_html(url):
    print(f"\nProcessando HTML de: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "Sem título"
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    print(f"Título da página: {title}")
    print("Links encontrados:")
    for link in links:
        print(f" - {link}")

def process_pdf(file_path):
    print(f"\n📄 Processando PDF: {file_path}")
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc, 1):
        text = page.get_text().strip()
        if text:
            print(f"\n--- Página {page_num} ---\n{text}")
    doc.close()

def process_image(file_path):
    print(f"\n Processando imagem: {file_path}")
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    print(f"\nTexto extraído:\n{text.strip()}")

def detect_and_process(path_or_url):
    if path_or_url.startswith("http"):
        # URL: assumimos HTML
        process_html(path_or_url)
    else:
        mime_type, _ = mimetypes.guess_type(path_or_url)
        if mime_type is None:
            print("Tipo de arquivo não identificado.")
            return

        if "pdf" in mime_type:
            process_pdf(path_or_url)
        elif "image" in mime_type:
            process_image(path_or_url)
        else:
            print(f"Tipo de arquivo não suportado: {mime_type}")

# HTML
detect_and_process("https://example.com")

# PDF
detect_and_process("https://www.nasa.gov/sites/default/files/atoms/files/nasa_exploration_plan.pdf")

# Imagem
detect_and_process("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/800px-PNG_transparency_demonstration_1.png")
