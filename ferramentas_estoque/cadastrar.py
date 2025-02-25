import streamlit as st
from banco.bd import create_db_estoque, insert_data_estoque

st.title("Cadastrar Ferramenta")
st.write("Cadastre novas ferramentas no estoque.")


# Campos do formulário
nome_ferram = st.text_input("Nome da Ferramenta")  # Nome da Ferramenta
quantidade = st.number_input("Quantidade", min_value=0, step=1)  # Quantidade no estoque
origem = st.text_input("Origem")  # Origem (ex.: Máxima ou Ferramentaria)
tempo_uso = st.number_input("Tempo de Uso (em dias)", min_value=0, step=1)  # Tempo de uso
tipo = st.selectbox("Tipo de Ferramenta", ["ELÉTRICA", "MANUAL", "PRECISÃO"])  # Lista suspensa para o tipo

if st.button("Cadastrar"):
    # Tratamento de erro para os campos obrigatórios e numéricos
    error_message = ""
    if nome_ferram.strip() == "":
        error_message += "O nome da ferramenta é obrigatório. "
    if quantidade <= 0:
        error_message += "A quantidade deve ser maior que zero. "
    if tempo_uso < 0:
        error_message += "O tempo de uso deve ser zero ou positivo. "
    if origem.strip() == "":
        error_message += "A origem é obrigatória. "

    if error_message:
        st.error(error_message)
    else:
        try:
            # Insere os dados na tabela "estoque_samarco" com os seguintes mapeamentos:
            #   qtd_est        ← quantidade
            #   qtd_ferramenta ← quantidade
            #   origem         ← origem
            #   nome_ferram    ← nome da ferramenta
            #   tempo_uso      ← tempo de uso
            #   tipo           ← valor selecionado na lista suspensa
            insert_data_estoque(
                "estoque_samarco",
                int(quantidade),
                int(quantidade),
                origem,
                nome_ferram,
                int(tempo_uso),
                tipo
            )
            st.success(f"Ferramenta '{nome_ferram}' cadastrada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao cadastrar a ferramenta: {e}")
