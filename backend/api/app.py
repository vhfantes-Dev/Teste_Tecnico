from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List
from pydantic import BaseModel

class Operadora(BaseModel):
    Registro_ANS: str
    CNPJ: str
    Razao_Social: str
    Nome_Fantasia: str
    Modalidade: str
    Logradouro: str
    Numero: str
    Complemento: str
    Bairro: str
    Cidade: str
    UF: str
    CEP: str
    DDD: str
    Telefone: str
    Fax: str
    Endereco_eletronico: str
    Representante: str
    Cargo_Representante: str
    Regiao_de_Comercializacao: str
    Data_Registro_ANS: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_PATH = "C:/Users/vitor/Desktop/Teste_Tecnico/backend/data/op_ativas/Relatorio_cadop.csv"
dataframe = None

# Carrega os dados na inicialização do servidor
try:
    dataframe = pd.read_csv(CSV_PATH, encoding="utf-8", delimiter=";")
    
    # Exibe as primeiras linhas para depuração
    print("Dados carregados com sucesso!")
    print(dataframe.head())

    dataframe.columns = ["Registro_ANS", "CNPJ", "Razao_Social", "Nome_Fantasia", "Modalidade", "Logradouro", "Numero", 
                         "Complemento", "Bairro", "Cidade", "UF", "CEP", "DDD", "Telefone", "Fax", "Endereco_eletronico", 
                         "Representante", "Cargo_Representante", "Regiao_de_Comercializacao", "Data_Registro_ANS"]
except Exception as e:
    print("Erro ao carregar o CSV:", e)

@app.get("/razao-social", response_model=List[Operadora])
def search_operadoras(query: str = Query(..., min_length=2)):
    if dataframe is None:
        raise HTTPException(status_code=500, detail="Dados não carregados")
    
    # Limpando espaços 
    dataframe['Nome_Fantasia'] = dataframe['Nome_Fantasia'].str.strip()
    
    # Garantir que se o nome fantasia não existir, seja exibido como uma string vazia
    dataframe['Nome_Fantasia'] = dataframe['Nome_Fantasia'].fillna('')
    dataframe['Complemento'] = dataframe['Complemento'].fillna('') 
    
    # Converter as colunas numéricas para string
    cols_to_convert = ['Registro_ANS','CNPJ', 'CEP', 'DDD', 'Telefone', 'Fax', 'Regiao_de_Comercializacao']
    dataframe[cols_to_convert] = dataframe[cols_to_convert].astype(str)

    # busca pela Razao_Social
    resultados = dataframe[dataframe['Razao_Social'].str.contains(query, case=False, na=False)]
    
    # Erro caso não ache
    if resultados.empty:
        raise HTTPException(status_code=404, detail="Nenhuma operadora encontrada")
    
    # retornando dados em JSON
    return resultados.to_dict(orient="records")


@app.get("/cnpj", response_model=List[Operadora])
def search_operadoras(query: str = Query(..., min_length=2)):
    if dataframe is None:
        raise HTTPException(status_code=500, detail="Dados não carregados")
    
   
    dataframe['Nome_Fantasia'] = dataframe['Nome_Fantasia'].str.strip()
    
    
    dataframe['Nome_Fantasia'] = dataframe['Nome_Fantasia'].fillna('')
    dataframe['Complemento'] = dataframe['Complemento'].fillna('') 
    
    
    cols_to_convert = ['Registro_ANS','CNPJ', 'CEP', 'DDD', 'Telefone', 'Fax', 'Regiao_de_Comercializacao']
    dataframe[cols_to_convert] = dataframe[cols_to_convert].astype(str)

 
    resultados = dataframe[dataframe['CNPJ'].str.contains(query, case=False, na=False)]
    

    if resultados.empty:
        raise HTTPException(status_code=404, detail="Nenhuma operadora encontrada")
    
    # retornando dados em JSON
    return resultados.to_dict(orient="records")


@app.get("/registro-ans", response_model=List[Operadora])
def search_operadoras(query: str = Query(..., min_length=2)):
    if dataframe is None:
        raise HTTPException(status_code=500, detail="Dados não carregados")
    
   
    dataframe['Nome_Fantasia'] = dataframe['Nome_Fantasia'].str.strip()
    
    
    dataframe['Nome_Fantasia'] = dataframe['Nome_Fantasia'].fillna('')
    dataframe['Complemento'] = dataframe['Complemento'].fillna('') 
    
    
    cols_to_convert = ['Registro_ANS','CNPJ', 'CEP', 'DDD', 'Telefone', 'Fax', 'Regiao_de_Comercializacao']
    dataframe[cols_to_convert] = dataframe[cols_to_convert].astype(str)

 
    resultados = dataframe[dataframe['Registro_ANS'].str.contains(query, case=False, na=False)]
    

    if resultados.empty:
        raise HTTPException(status_code=404, detail="Nenhuma operadora encontrada")
    
    # retornando dados em JSON
    return resultados.to_dict(orient="records")


@app.get("/")
def root():
    return {"message": "API de Busca de Operadoras"}