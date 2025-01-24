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

st.title("Gráficos de Estoque")
st.write("Visualize gráficos relacionados ao estoque.")

# Gráfico de produtos mais movimentados
st.subheader("Produtos Mais Movimentados")
df_movimentacoes = exibir_movimentacoes()
if not df_movimentacoes.empty:
    produtos_movimentados = df_movimentacoes['nome'].value_counts().reset_index()
    produtos_movimentados.columns = ['nome', 'movimentacoes']
    st.bar_chart(produtos_movimentados.set_index('nome'))
else:
    st.warning("Nenhuma movimentação registrada.")

# Gráfico de estoque baixo
st.subheader("Produtos com Estoque Baixo")
df_estoque = exibir_estoque()
if not df_estoque.empty:
    estoque_baixo = df_estoque[df_estoque['quantidade'] < 10]  # Exemplo: estoque mínimo de 10
    if not estoque_baixo.empty:
        st.bar_chart(estoque_baixo.set_index('nome')['quantidade'])
    else:
        st.warning("Nenhum produto com estoque baixo.")
else:
    st.warning("Nenhum produto cadastrado.")