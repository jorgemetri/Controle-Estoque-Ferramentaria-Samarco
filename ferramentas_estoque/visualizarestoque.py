import streamlit as st
import sqlite3
import pandas as pd

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('estoque.db', check_same_thread=False)

# Função para exibir o estoque atual
def exibir_estoque():
    conn = connect_db()
    df = pd.read_sql('SELECT * FROM produtos', conn)
    conn.close()
    return df

st.title("Visualizar Estoque")
st.write("Visualize o estoque atual em formato de tabela.")

df = exibir_estoque()
if not df.empty:
    st.dataframe(df)
else:
    st.warning("Nenhum produto cadastrado.")