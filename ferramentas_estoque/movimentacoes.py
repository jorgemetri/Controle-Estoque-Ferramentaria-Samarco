import streamlit as st
import sqlite3
import pandas as pd

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('estoque.db', check_same_thread=False)

# Função para exibir movimentações
def exibir_movimentacoes():
    conn = connect_db()
    df = pd.read_sql('''
        SELECT m.id, p.nome, m.tipo, m.quantidade, m.data
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
    ''', conn)
    conn.close()
    return df

st.title("Movimentações")
st.write("Visualize o histórico de entradas e saídas de produtos.")

df = exibir_movimentacoes()
if not df.empty:
    st.dataframe(df)
else:
    st.warning("Nenhuma movimentação registrada.")