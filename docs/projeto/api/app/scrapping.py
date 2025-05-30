import os
from dotenv import load_dotenv
import requests
import psycopg2
import pandas as pd

# 1️⃣ Carrega as variáveis de .env
load_dotenv()

def pegar_dados_ibovespa():
    url = "https://www.infomoney.com.br/cotacoes/ibovespa/"
    response = requests.get(url)
    # Aqui adapte seu scraping real...
    return {"dados": "Últimos 10 dias do índice Bovespa (simulado)"}

def salvar_no_postgres(dados: dict):
    # 2️⃣ Monta a conexão usando as vars de ambiente
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    cur = conn.cursor()

    # 3️⃣ (Opcional) cria a tabela se não existir
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ibovespa (
        id SERIAL PRIMARY KEY,
        data_captura TIMESTAMP DEFAULT NOW(),
        valor TEXT
    );
    """)

    # 4️⃣ Insere o valor
    cur.execute(
        "INSERT INTO ibovespa (valor) VALUES (%s);",
        (dados["dados"],)
    )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    dados = pegar_dados_ibovespa()
    salvar_no_postgres(dados)
    print("Dados gravados com sucesso!")
