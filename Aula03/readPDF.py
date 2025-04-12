from PyPDF2 import PdfReader

reader = PdfReader("2025.1_alocacao.pdf")
for page in reader.pages:
    print(page.extract_text())