import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import zipfile
import os
import csv
from tabulate import tabulate

DIR_CONTABEIS = "C:/Users/vitor/Desktop/Teste_Tecnico/backend/data/dados_contabeis"
DIR_OPERADORAS = "C:/Users/vitor/Desktop/Teste_Tecnico/backend/data/op_ativas"

def extrair_zip():
    # Extração dos arquivos em ZIP da pasta dados_contabeis
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
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  
        dados = []
        
        for row in reader:
            row_tratada = [None if valor == '' else valor for valor in row] # Substitui valor vazio por none
            if len(row_tratada) == campos:
                dados.append(tuple(row_tratada))
            else:
                print(f"Erro na linha {reader.line_num}: número de colunas inválido.")
            
            # Limitando o fluxo de dados
            if len(dados) >= 20000:
                cursor.executemany(query, dados)
                dados.clear()
                print(f"✅ Lote de 20000 registros de {csv_path} importado.")
        
        # Insere os dados restantes (caso haja menos de 20000 registros)
        if dados:
            cursor.executemany(query, dados)
            print(f"✅ Dados restantes de {csv_path} importados.")

def importar_csv_contabeis():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for arquivo in os.listdir(DIR_CONTABEIS):
            if arquivo.endswith(".csv"):
                csv_path = os.path.join(DIR_CONTABEIS, arquivo)
                query = """
                    INSERT INTO demonstracoes_contabeis (data_referencia, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                processar_csv(csv_path, query, 6, cursor)

        conn.commit()  
        print("✅ Todos os arquivos CSV foram importados com sucesso.")
        
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

def importar_csv_operadoras():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        
        for arquivo in os.listdir(DIR_OPERADORAS):
            if arquivo.endswith(".csv"):
                csv_path = os.path.join(DIR_OPERADORAS, arquivo)
                query = """
                    INSERT INTO operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, 
                    complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, 
                    representante, cargo_representante, regiao_comercializacao, data_registro_ans)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                processar_csv(csv_path, query, 20, cursor)

        conn.commit()
        print("✅ Todos os arquivos CSV de operadoras foram importados com sucesso.")
        
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()
def executar_consultas():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    

    consulta_trimestre = """
      SELECT 
      reg_ans, 
      SUM(vl_saldo_final) AS total_despesas
      FROM demonstracoes_contabeis
      WHERE data_referencia >= NOW() - INTERVAL 3 MONTH
      AND (descricao LIKE '%sinistro%' 
      OR descricao LIKE '%evento%' 
      OR descricao LIKE '%assistência%' 
      OR descricao LIKE '%saúde%')
      GROUP BY reg_ans
      ORDER BY total_despesas DESC
    LIMIT 10;

    """
    print("📊 Top 10 operadoras (último trimestre):")
    cursor.execute(consulta_trimestre)
    resultados_trimestre = cursor.fetchall()
    colunas_trimestre = [desc[0] for desc in cursor.description]
    print(tabulate(resultados_trimestre, headers=colunas_trimestre, tablefmt='grid'))
    
    consulta = """
        SELECT 
            reg_ans, 
            SUM(vl_saldo_final) AS total_despesas
        FROM demonstracoes_contabeis
        WHERE data_referencia >= NOW() - INTERVAL 1 YEAR
        AND (descricao LIKE '%sinistro%' 
            OR descricao LIKE '%evento%' 
            OR descricao LIKE '%assistência%' 
            OR descricao LIKE '%saúde%')
        GROUP BY reg_ans
        ORDER BY total_despesas DESC
        LIMIT 10;
        """

    cursor.execute(consulta)
    resultados = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    
    print("📊 Top 10 operadoras (último ano):")
    print(tabulate(resultados, headers=colunas, tablefmt='grid'))

    cursor.close()
    conn.close()