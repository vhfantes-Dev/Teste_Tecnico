import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import zipfile
import os
import csv

DIR_CONTABEIS = "C:/Users/vitor/Desktop/Teste_Tecnico/backend/data/dados_contabeis"
DIR_OPERADORAS = "C:/Users/vitor/Desktop/Teste_Tecnico/backend/data/op_ativas"

def extrair_zip():
    # Extração dos arquivos ZIP da pasta dados_contabeis
    for zip_file in os.listdir(DIR_CONTABEIS):
        if zip_file.endswith(".zip"):
            zip_path = os.path.join(DIR_CONTABEIS, zip_file)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(DIR_CONTABEIS)
                print(f"📂 Arquivos extraídos de {zip_path} para {DIR_CONTABEIS}")
        
def criar_tabelas(): # criação das tabelas
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data_referencia DATE,
        reg_ans VARCHAR(50),
        cd_conta_contabil VARCHAR(50),
        descricao TEXT,
        vl_saldo_inicial DECIMAL(18,2),
        vl_saldo_final DECIMAL(18,2)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operadoras (
        id INT AUTO_INCREMENT PRIMARY KEY,
        registro_ans VARCHAR(50) UNIQUE,
        cnpj VARCHAR(20),
        razao_social VARCHAR(255),
        nome_fantasia VARCHAR(255),
        modalidade VARCHAR(100),
        logradouro TEXT,
        numero VARCHAR(10),
        complemento TEXT,
        bairro VARCHAR(100),
        cidade VARCHAR(100),
        uf VARCHAR(10),
        cep VARCHAR(15),
        ddd VARCHAR(5),
        telefone VARCHAR(20),
        fax VARCHAR(20),
        endereco_eletronico TEXT,
        representante VARCHAR(255),
        cargo_representante VARCHAR(100),
        regiao_comercializacao TEXT,
        data_registro_ans DATE
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tabelas criadas com sucesso!")

def processar_csv(csv_path, query, campos, cursor):
    """Processa os arquivos CSV em lotes para importação no banco de dados."""
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Ignora o cabeçalho
        dados = []
        
        for row in reader:
            # Substitui valores vazios (ou faltando) por None
            row_tratada = [None if valor == '' else valor for valor in row]
            
            # Verifica se o número de campos está correto
            if len(row_tratada) == campos:
                dados.append(tuple(row_tratada))
            else:
                print(f"Erro na linha {reader.line_num}: número de colunas inválido.")
            
            # Limite o tamanho do lote para 20000 (ajuste conforme necessário)
            if len(dados) >= 20000:
                cursor.executemany(query, dados)
                dados.clear()  # Limpa os dados para o próximo lote
                print(f"✅ Lote de 20000 registros de {csv_path} importado.")
        
        # Insere os dados restantes (caso haja menos de 20000 registros)
        if dados:
            cursor.executemany(query, dados)
            print(f"✅ Dados restantes de {csv_path} importados.")

def importar_csv_contabeis():
    """Importa os arquivos CSV da pasta de dados contábeis para o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Desabilita auto-commit para melhorar a performance
        conn.autocommit = False

        for arquivo in os.listdir(DIR_CONTABEIS):
            if arquivo.endswith(".csv"):
                csv_path = os.path.join(DIR_CONTABEIS, arquivo)
                query = """
                    INSERT INTO demonstracoes_contabeis (data_referencia, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                processar_csv(csv_path, query, 6, cursor)  # São 6 campos para cada linha

        conn.commit()  # Confirma todas as transações de uma vez
        print("✅ Todos os arquivos CSV foram importados com sucesso.")
        
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

def importar_csv_operadoras():
    """Importa os arquivos CSV da pasta de operadoras para o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Desabilita auto-commit para melhorar a performance
        conn.autocommit = False

        for arquivo in os.listdir(DIR_OPERADORAS):
            if arquivo.endswith(".csv"):
                csv_path = os.path.join(DIR_OPERADORAS, arquivo)
                query = """
                    INSERT INTO operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, 
                    complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, 
                    representante, cargo_representante, regiao_comercializacao, data_registro_ans)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                processar_csv(csv_path, query, 20, cursor)  # São 19 campos para cada linha

        conn.commit()  # Confirma todas as transações de uma vez
        print("✅ Todos os arquivos CSV de operadoras foram importados com sucesso.")
        
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()
