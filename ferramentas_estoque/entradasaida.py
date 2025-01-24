import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('estoque.db', check_same_thread=False)

# Função para buscar produtos
def buscar_produtos(nome=None):
    conn = connect_db()
    query = 'SELECT * FROM produtos'
    if nome:
        query += f" WHERE nome LIKE '%{nome}%'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Função para registrar uma movimentação
def add_movimentacao(produto_id, tipo, quantidade, data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, data)
        VALUES (?, ?, ?, ?)
    ''', (produto_id, tipo, quantidade, data))
    conn.commit()
    conn.close()

# Função para atualizar a quantidade de um produto
def update_quantidade(produto_id, quantidade):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade + ?
        WHERE id = ?
    ''', (quantidade, produto_id))
    conn.commit()
    conn.close()

st.title("Entrada/Saída de Produtos")
st.write("Registre entradas e saídas de produtos no estoque.")

# Barra de pesquisa para selecionar o produto
search_term = st.text_input("Pesquisar Produto")
produtos = buscar_produtos(nome=search_term)

if not produtos.empty:
    produto_id = st.selectbox(
        "Selecione o Produto",
        produtos['id'],
        format_func=lambda x: produtos[produtos['id'] == x]['nome'].values[0]
    )
    tipo = st.selectbox("Tipo", ["entrada", "saida"])
    quantidade = st.number_input("Quantidade", min_value=1)
    data = st.date_input("Data")
    if st.button("Registrar"):
        add_movimentacao(produto_id, tipo, quantidade, str(data))
        update_quantidade(produto_id, quantidade if tipo == 'entrada' else -quantidade)
        st.success(f"Movimentação registrada com sucesso!")
else:
    st.warning("Nenhum produto encontrado.")