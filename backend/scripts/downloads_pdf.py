import requests
import os
from bs4 import BeautifulSoup

URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

def baixar_pdfs():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Coletar todos os links de PDF
    pdf_links = [link["href"] for link in soup.find_all("a", href=True) if link["href"].endswith(".pdf")]
    
    # Exibir todos os links de PDF para depuração
    print(f"Todos os links de PDF encontrados: {pdf_links}")

    # Filtrar links que contêm "Anexo I" ou "Anexo II"
    anexos = ["Anexo_I", "Anexo_II"]
    pdf_links_filtrados = [link for link in pdf_links if any(anexo.lower() in link.lower() for anexo in anexos)]
    
    # Exibir links filtrados para depuração
    print(f"Links filtrados: {pdf_links_filtrados}")

    baixados = []

    for link in pdf_links_filtrados:
        if not link.startswith("http"):
            link = "https://www.gov.br" + link

        file_name = link.split("/")[-1]
        file_path = os.path.join("data/downloads", file_name)

        pdf_response = requests.get(link)
        pdf_response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(pdf_response.content)
            baixados.append(file_path)
        print(f"📥 Baixado: {file_name}")

    return baixados
