import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from downloads_pdf import baixar_pdfs 

def main():
    print("🔍 Iniciando o download dos PDFs...")
    arquivos_baixados = baixar_pdfs()
    
    if arquivos_baixados:
        print("\n✅ Download concluído! Arquivos salvos em:")
        for arquivo in arquivos_baixados:
            print(f" - {arquivo}")
    else:
        print("\n⚠ Nenhum arquivo foi baixado.")

if __name__ == "__main__":
    main()
