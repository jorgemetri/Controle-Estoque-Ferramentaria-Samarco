import streamlit as st
import sqlite3

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('estoque.db', check_same_thread=False)

# Função para adicionar um produto
def add_produto(nome, quantidade, preco, categoria, fornecedor):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, quantidade, preco, categoria, fornecedor)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, quantidade, preco, categoria, fornecedor))
    conn.commit()
    conn.close()

st.title("Cadastrar Produto")
st.write("Cadastre novos produtos no estoque.")

# Campos do formulário
nome = st.text_input("Nome do Produto")
quantidade = st.number_input("Quantidade", min_value=0)
preco = st.number_input("Preço", min_value=0.0)
categoria = st.text_input("Categoria")
fornecedor = st.text_input("Fornecedor")

if st.button("Cadastrar"):
    add_produto(nome, quantidade, preco, categoria, fornecedor)
    st.success(f"Produto '{nome}' cadastrado com sucesso!")