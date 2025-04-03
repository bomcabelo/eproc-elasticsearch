from elasticsearch import Elasticsearch
import mysql.connector
import os

# Configuração do Banco de Dados
db_host = os.getenv("DB_HOST", "10.33.1.114")
db_name = os.getenv("DB_NAME", "eproctjto_prod_1grau")
db_user = os.getenv("DB_USER", "eprocv2teste")
db_password = os.getenv("DB_PASSWORD", "T3st4nd@3309x")
db_port = os.getenv("DB_PORT", "3307")

# Configuração do Elasticsearch
es_host = os.getenv("ES_HOST", "http://elasticsearch:9200")
es_index = os.getenv("ES_INDEX", "indice_eproc")

try:
    # Conectar ao banco de dados
    connection = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )

    if connection.is_connected():
        print(f"✅ Conectado ao banco de dados {db_name}!")

        cursor = connection.cursor()
        cursor.execute("""
            SELECT id_classe_judicial, cod_classe, des_classe
            FROM eproctjto_prod_2grau.classe_judicial
            LIMIT 500;
        """)
        
        dados = cursor.fetchall()
        es = Elasticsearch([es_host])

        # Indexar dados no Elasticsearch
        for registro in dados:
            documento = {
                "id_classe_judicial": registro[0],
                "cod_classe": registro[1],
                "des_classe": registro[2],
            }
            es.index(index=es_index, document=documento)

        print(f"✅ {len(dados)} registros indexados no Elasticsearch!")
        cursor.close()

except mysql.connector.Error as err:
    print(f"❌ Erro ao conectar ao MySQL: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("✅ Conexão com MySQL encerrada.")
