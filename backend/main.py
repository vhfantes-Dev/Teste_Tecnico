import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from downloads_pdf import baixar_pdfs 
from extract_data import processar_pdf
from database import extrair_zip
from database import importar_csv_contabeis
from database import importar_csv_operadoras

def main():
    print("🔍 Iniciando o download dos PDFs...")
    arquivos_baixados = baixar_pdfs()
    
    if arquivos_baixados:
        print("\n✅ Download concluído! Arquivos salvos em:")
        for arquivo in arquivos_baixados:
            print(f" - {arquivo}")
        print("Dados sendo processados...")
        processar_pdf(arquivos_baixados)   
    else:
        print("\n⚠ Nenhum arquivo foi baixado.")
        
    print("\n🔄 Iniciando exportação de arquivos CSV contábeis...")
    extrair_zip()
    print("\n🔄 Iniciando importação de arquivos CSV contábeis...")
    importar_csv_contabeis()

    print("\n🔄 Iniciando importação de arquivos CSV de operadoras...")
    importar_csv_operadoras()
    
if __name__ == "__main__":
    main()
