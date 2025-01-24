import streamlit as st
import sqlite3
import pandas as pd

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('estoque.db', check_same_thread=False)

# Função para buscar produtos
def buscar_produtos(nome=None, categoria=None):
    conn = connect_db()
    query = 'SELECT * FROM produtos'
    conditions = []
    if nome:
        conditions.append(f"nome LIKE '%{nome}%'")
    if categoria:
        conditions.append(f"categoria = '{categoria}'")
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Buscar Produto")
st.write("Busque produtos no estoque por nome ou categoria.")

# Campos de busca
nome = st.text_input("Nome do Produto")
categoria = st.text_input("Categoria")

if st.button("Buscar"):
    df = buscar_produtos(nome, categoria)
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("Nenhum produto encontrado.")