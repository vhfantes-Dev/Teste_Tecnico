import pdfplumber
import pandas as pd
import os
import zipfile

def extrair_tabela_pdf(pdf_path):
    dados = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tabela = page.extract_table()
            if tabela:
                for linha in tabela:
                    dados.append(linha)
    return pd.DataFrame(dados)

def processar_pdf(baixados):
    anexo_i_path = next((file for file in baixados if "Anexo_I" in file),None)
    if not anexo_i_path:
        print("Anexo I não encontrado!")
        return
    df= extrair_tabela_pdf(anexo_i_path)
    if not df.empty:
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.rename(columns={"OD" : "Odontolígico","AMB": "Ambulatorial"})
        
        #Salvando arquivo em csv
        csv_path = "data/transformed/rol_procedimentos.csv" 
        df.to_csv(csv_path, index=False, encoding="utf-8")
        #Compactando arquivo em zip
        zip_filename ="Teste_Vitor_Henrique_Fantes.zip"
        zip_path = os.path.join("data", "transformed", zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))  
        print(f"Arquivo ZIP gerado: {zip_path}")
        print(f"Dados salvos em: {csv_path}")
    else:
        print("Erro: Não foi possível extrair a tabela do PDF.")