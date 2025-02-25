import streamlit as st
import sqlite3
import pandas as pd
from banco.bd import search_product_by_name_estoque  # Função para buscar na tabela de estoque

st.title("Buscar Ferramenta")
st.write("Busque ferramentas e visualize seus registros no estoque e nas movimentações.")

# Campo de busca
nome_busca = st.text_input("Digite o nome da ferramenta para buscar:")

if st.button("Buscar"):
    try:
        # Busca na tabela de estoque (supondo que a coluna seja 'nome_ferram')
        df_estoque = search_product_by_name_estoque("estoque_samarco", nome_busca)
        
        # Busca na tabela de movimentações (a coluna referente ao nome da ferramenta é 'nome_ferramenta')
        conn = sqlite3.connect("movimentacao_samarco.db", check_same_thread=False)
        query = "SELECT * FROM movimentacao_samarco WHERE nome_ferramenta LIKE ?"
        df_movimentacao = pd.read_sql_query(query, conn, params=(f"%{nome_busca}%",))
        conn.close()
        
        st.subheader("Resultados no Estoque")
        if df_estoque.empty:
            st.warning("Nenhuma ferramenta encontrada no estoque.")
        else:
            st.dataframe(df_estoque, use_container_width=True)
        
        st.subheader("Resultados nas Movimentações")
        if df_movimentacao.empty:
            st.warning("Nenhuma movimentação encontrada para essa ferramenta.")
        else:
            st.dataframe(df_movimentacao, use_container_width=True)
    
    except Exception as e:
        st.error(f"Erro ao buscar ferramenta: {e}")
