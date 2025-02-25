import streamlit as st
from banco.bd import (
    create_db_movimentacao,
    get_db_as_dataframe,
    insert_data_movimentacao,
    update_data_movimentacao,
    remove_data_movimentacao
)

st.title("Gerenciamento de Movimentação")
st.write("Realize operações de inserção, atualização, remoção e visualização de registros na tabela 'movimentacao_samarco'.")

# Cria o banco de dados e a tabela
if st.button("Criar Banco"):
    create_db_movimentacao("movimentacao_samarco")

st.markdown("---")

# Exemplo de Inserção
if st.button("Inserir Registro"):
    # Exemplo:
    # - nome_pessoa: "João Silva"
    # - matricula: 12345
    # - data: "2025-02-25" (formato YYYY-MM-DD)
    # - email_solicitante: "joao@exemplo.com"
    # - email_gestor: "gestor@exemplo.com"
    # - movimentacao: "Entrada" (movimentacao é TEXT)
    # - qtd_mov: 10
    # - codigo_ferramenta: 101
    # - nome_ferramenta: "Martelo"
    insert_data_movimentacao(
        "movimentacao_samarco",
        "João Silva",
        12345,
        "2025-02-25",
        "joao@exemplo.com",
        "gestor@exemplo.com",
        "Entrada",
        10,
        101,
        "Martelo"
    )
    st.write("Registro inserido com sucesso!")

st.markdown("---")

# Exemplo de Atualização
if st.button("Atualizar Registro"):
    # Exemplo: Atualiza o registro com id=1
    # Alterando nome para "João Oliveira", data para "2025-02-26",
    # movimentacao para "Saída", qtd_mov para 15, codigo_ferramenta para 102 
    # e nome_ferramenta para "Chave de Fenda"
    update_data_movimentacao(
        "movimentacao_samarco",
        1,
        "João Oliveira",
        12345,
        "2025-02-26",
        "joao@exemplo.com",
        "gestor@exemplo.com",
        "Saída",
        15,
        102,
        "Chave de Fenda"
    )
    st.write("Registro atualizado com sucesso!")

st.markdown("---")

# Exemplo de Remoção
if st.button("Remover Registro"):
    # Remove o registro com id=1
    remove_data_movimentacao("movimentacao_samarco", 1)
    st.write("Registro removido com sucesso!")

st.markdown("---")

# Exibe todos os registros das tabelas em um DataFrame
if st.button("Exibir Dados"):
    try:
        df1 = get_db_as_dataframe("estoque_samarco")
        df2 = get_db_as_dataframe("movimentacao_samarco")
        st.dataframe(df1)
        st.dataframe(df2)
    except Exception as e:
        st.error(f"Erro ao exibir dados: {e}")
