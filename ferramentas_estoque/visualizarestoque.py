import streamlit as st
import sqlite3
import pandas as pd
from banco.bd import connect_db  # Certifique-se de que essa função esteja definida no módulo

# Função para exibir o estoque atual a partir da tabela 'estoque_samarco'
def exibir_estoque():
    conn = connect_db("estoque_samarco")
    df = pd.read_sql_query("SELECT * FROM estoque_samarco", conn)
    conn.close()
    return df

st.title("Visualizar Estoque")
st.write("Visualize o estoque atual em formato de tabela.")

df = exibir_estoque()
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Nenhum produto cadastrado.")
