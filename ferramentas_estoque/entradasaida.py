import streamlit as st
import sqlite3
import pandas as pd
from banco.bd import (
    create_db_movimentacao,
    get_db_as_dataframe,
    insert_data_movimentacao,
    update_data_movimentacao,
    remove_data_movimentacao,
    search_product_by_name_estoque,
    update_data_estoque  # Função para atualizar a tabela de estoque
)

st.title("Registro de Movimentação de Ferramentas")
st.write("Registre movimentações (Empréstimo ou Devolução) na tabela 'movimentacao_samarco'.")

# --- Seção de Pesquisa no Estoque ---
st.header("Pesquisar Ferramenta no Estoque")
product_search = st.text_input("Digite o nome da ferramenta para pesquisar:")

if st.button("Pesquisar"):
    try:
        df_search = search_product_by_name_estoque("estoque_samarco", product_search)
        if df_search.empty:
            st.warning("Nenhuma ferramenta encontrada com esse nome.")
        else:
            st.dataframe(df_search)
    except Exception as e:
        st.error(f"Erro ao buscar ferramenta: {e}")

st.markdown("---")

# --- Abas para operações de movimentação ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Registrar movimentação", 
    "Atualizar Movimentacao", 
    "Remover Movimentacao",
    "Exibir Movimentações"
])

with tab1:
    st.header("Registrar movimentação")
    nome_pessoa = st.text_input("Nome da Pessoa")
    matricula = st.number_input("Matrícula", min_value=0, step=1)
    data = st.date_input("Data")
    email_solicitante = st.text_input("Email do Solicitante")
    email_gestor = st.text_input("Email do Gestor")
    movimentacao = st.selectbox("Tipo de Movimentação", ["Empréstimo", "Devolução"])
    qtd_mov = st.number_input("Quantidade Movimentada", min_value=1, step=1)
    codigo_ferramenta = st.number_input("Código da Ferramenta", min_value=0, step=1)
    nome_ferramenta = st.text_input("Nome da Ferramenta")
    
    if st.button("Registrar Movimentação", key="registra_mov"):
        try:
            # Consulta o estoque disponível na tabela 'estoque_samarco'
            conn = sqlite3.connect("estoque_samarco.db", check_same_thread=False)
            cur = conn.cursor()
            # Seleciona todos os campos necessários do registro de estoque (supondo um único registro)
            cur.execute("""
                SELECT id, qtd_est, qtd_ferramenta, origem, nome_ferram, tempo_uso, tipo 
                FROM estoque_samarco LIMIT 1
            """)
            row = cur.fetchone()
            conn.close()
            
            if not row:
                st.error("Estoque não encontrado na tabela 'estoque_samarco'.")
            else:
                estoque_id, qtd_est_db, qtd_ferramenta_db, origem_db, nome_ferram_db, tempo_uso_db, tipo_db = row

                if movimentacao == "Empréstimo":
                    # Para empréstimo, a quantidade solicitada deve ser menor ou igual à quantidade disponível
                    if qtd_mov > 0 and qtd_mov <= qtd_ferramenta_db:
                        insert_data_movimentacao(
                            "movimentacao_samarco",
                            nome_pessoa,
                            matricula,
                            data.strftime("%Y-%m-%d"),
                            email_solicitante,
                            email_gestor,
                            movimentacao,
                            qtd_mov,
                            codigo_ferramenta,
                            nome_ferramenta
                        )
                        # Atualiza o estoque: subtrai a quantidade emprestada
                        new_qtd_ferramenta = qtd_ferramenta_db - qtd_mov
                        update_data_estoque(
                            "estoque_samarco",
                            estoque_id,
                            qtd_est_db,
                            new_qtd_ferramenta,
                            origem_db,
                            nome_ferram_db,
                            tempo_uso_db,
                            tipo_db
                        )
                        st.success("Movimentação registrada e estoque atualizado com sucesso!")
                    else:
                        st.error("Para Empréstimo, a quantidade deve ser maior que zero e não exceder a quantidade disponível no estoque.")
                elif movimentacao == "Devolução":
                    # Para devolução, a quantidade a ser devolvida não pode exceder o que foi emprestado,
                    # isto é, a diferença entre o estoque total (qtd_est) e o estoque atual (qtd_ferramenta)
                    if (qtd_est_db - qtd_ferramenta_db) >= qtd_mov:
                        insert_data_movimentacao(
                            "movimentacao_samarco",
                            nome_pessoa,
                            matricula,
                            data.strftime("%Y-%m-%d"),
                            email_solicitante,
                            email_gestor,
                            movimentacao,
                            qtd_mov,
                            codigo_ferramenta,
                            nome_ferramenta
                        )
                        # Atualiza o estoque: adiciona a quantidade devolvida
                        new_qtd_ferramenta = qtd_ferramenta_db + qtd_mov
                        update_data_estoque(
                            "estoque_samarco",
                            estoque_id,
                            qtd_est_db,
                            new_qtd_ferramenta,
                            origem_db,
                            nome_ferram_db,
                            tempo_uso_db,
                            tipo_db
                        )
                        st.success("Movimentação registrada e estoque atualizado com sucesso!")
                    else:
                        st.error("Para Devolução, a quantidade excede o limite disponível para retorno.")
                else:
                    st.error("Tipo de movimentação inválido.")
        except Exception as e:
            st.error(f"Erro ao registrar movimentação: {e}")

with tab2:
    st.header("Atualizar Movimentacao")
    record_id = st.number_input("ID do Registro a Atualizar", min_value=1, step=1, key="update_id")
    novo_nome_pessoa = st.text_input("Novo Nome da Pessoa", key="update_nome")
    nova_matricula = st.number_input("Nova Matrícula", min_value=0, step=1, key="update_matricula")
    nova_data = st.date_input("Nova Data", key="update_data")
    novo_email_solicitante = st.text_input("Novo Email do Solicitante", key="update_email_solicitante")
    novo_email_gestor = st.text_input("Novo Email do Gestor", key="update_email_gestor")
    novo_movimentacao = st.selectbox("Novo Tipo de Movimentação", ["Empréstimo", "Devolução"], key="update_mov")
    novo_qtd_mov = st.number_input("Nova Quantidade Movimentada", min_value=1, step=1, key="update_qtd_mov")
    novo_codigo_ferramenta = st.number_input("Novo Código da Ferramenta", min_value=0, step=1, key="update_codigo")
    novo_nome_ferramenta = st.text_input("Novo Nome da Ferramenta", key="update_nome_ferramenta")
    
    if st.button("Atualizar Registro", key="update_button"):
        try:
            update_data_movimentacao(
                "movimentacao_samarco",
                record_id,
                novo_nome_pessoa,
                nova_matricula,
                nova_data.strftime("%Y-%m-%d"),
                novo_email_solicitante,
                novo_email_gestor,
                novo_movimentacao,
                novo_qtd_mov,
                novo_codigo_ferramenta,
                novo_nome_ferramenta
            )
            st.success("Registro de movimentação atualizado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao atualizar registro: {e}")

with tab3:
    st.header("Remover Movimentacao")
    remove_id = st.number_input("ID do Registro a Remover", min_value=1, step=1, key="remove_id")
    
    if st.button("Remover Registro", key="remove_button"):
        try:
            remove_data_movimentacao("movimentacao_samarco", remove_id)
            st.success("Registro de movimentação removido com sucesso!")
        except Exception as e:
            st.error(f"Erro ao remover registro: {e}")

with tab4:
    st.header("Exibir Movimentações")
    
    if st.button("Exibir Dados", key="exibir_button"):
        try:
            df = get_db_as_dataframe("movimentacao_samarco")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erro ao exibir dados: {e}")
