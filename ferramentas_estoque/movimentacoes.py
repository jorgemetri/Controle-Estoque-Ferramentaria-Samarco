import streamlit as st


import pandas as pd
from banco.bd import get_db_as_dataframe

st.title("Histórico de Movimentações")
st.write("Visualize o histórico completo de entradas e saídas de ferramentas.")

try:
    df = get_db_as_dataframe("movimentacao_samarco")
    
    if df.empty:
        st.warning("Nenhuma movimentação registrada.")
    else:
        st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao exibir movimentações: {e}")
