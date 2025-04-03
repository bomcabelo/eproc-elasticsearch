import streamlit as st
from elasticsearch import Elasticsearch
import os

# Conectar ao Elasticsearch
es_host = os.getenv("ES_HOST", "http://elasticsearch:9200")
es = Elasticsearch([es_host])

st.title("🔎 Consulta ao Banco de Dados eProc")

# Entrada do usuário
query = st.text_input("Digite o código da classe:")

if query:
    try:
        resposta = es.search(index="indice_eproc", body={"query": {"match": {"cod_classe": query}}})
        st.json(resposta["hits"]["hits"])
    except Exception as e:
        st.error(f"Erro na busca: {e}")
