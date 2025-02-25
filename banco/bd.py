import sqlite3
import streamlit as st
import os
import pandas as pd

def create_db_estoque(name):
    """
    args: 
        name: Nome do banco de dados (sem extensão) e também o nome da tabela a ser criada.
    Campos do banco:
    - id: Id único.
    - qtd_est:  inteiro.
    - qtd_ferramenta: inteiro.
    - origem: string.
    - nome_ferram: string.
    - tempo_uso: inteiro.
    - tipo: string.
    """
    db_file = f"{name}.db"
    
    # Verifica se o banco de dados já existe
    if os.path.exists(db_file):
        st.write(f"O banco de dados '{db_file}' já existe.")
        return
    
    # Cria a conexão com o banco de dados
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Cria a tabela com o nome passado na função
    cursor.execute(f'''
        CREATE TABLE {name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qtd_est INTEGER,
            qtd_ferramenta INTEGER,
            origem TEXT,
            nome_ferram TEXT,
            tempo_uso INTEGER,
            tipo TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    st.write(f"O banco de dados '{db_file}' e a tabela '{name}' foram criados com sucesso.")


#Função utilizada para se conectar aos dados do banco------------------------------------------------------------------------------------------------------------------------
def connect_db(name):
    """
    Conecta ao banco de dados SQLite com o nome especificado.

    Args:
        name (str): Nome do banco de dados (sem extensão).

    Returns:
        Connection: objeto de conexão com o banco de dados ou None em caso de erro.
    """
    try:
        connection = sqlite3.connect(f'{name}.db', check_same_thread=False)
        return connection
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
#Função responsável por retornar dados do banco como se fosse um dataframe---------------------------------------------------------------------------------------------
def get_db_as_dataframe(name):
    """
    Conecta ao banco de dados e retorna todo o conteúdo da tabela cujo nome é o mesmo passado em 'name'
    como um DataFrame do pandas.

    Args:
        name (str): Nome do banco de dados (sem a extensão .db) e também o nome da tabela.

    Returns:
        DataFrame: DataFrame contendo todos os registros da tabela com nome 'name'.

    Raises:
        Exception: Caso não seja possível conectar ao banco de dados
                   ou consultar a tabela.
    """
    conn = connect_db(name)
    if conn is None:
        raise Exception("Erro ao conectar ao banco de dados")
    
    try:
        query = f"SELECT * FROM {name}"
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        raise Exception(f"Erro ao consultar a tabela '{name}': {e}")
    finally:
        conn.close()
    
    return df

def insert_data_estoque(name, qtd_est, qtd_ferramenta, origem, nome_ferram, tempo_uso, tipo):
    """
    Insere um novo registro na tabela cujo nome é o mesmo passado em 'name'.
    
    Args:
        name (str): Nome do banco de dados (sem extensão .db) e também nome da tabela.
        qtd_est (int): Quantidade de estoque.
        qtd_ferramenta (int): Quantidade de ferramentas.
        origem (str): Origem.
        nome_ferram (str): Nome da ferramenta.
        tempo_uso (int): Tempo de uso.
        tipo (str): Tipo.
        
    Raises:
        Exception: Caso ocorra um erro ao inserir os dados.
    """
    conn = connect_db(name)
    if conn is None:
        raise Exception("Erro ao conectar ao banco de dados")
    
    try:
        cursor = conn.cursor()
        query = f"INSERT INTO {name} (qtd_est, qtd_ferramenta, origem, nome_ferram, tempo_uso, tipo) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (qtd_est, qtd_ferramenta, origem, nome_ferram, tempo_uso, tipo))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()


def remove_data_estoque(name, record_id):
    """
    Remove um registro da tabela cujo nome é o mesmo passado em 'name', baseado no id.
    
    Args:
        name (str): Nome do banco de dados (sem extensão .db) e também nome da tabela.
        record_id (int): ID do registro a ser removido.
    
    Raises:
        Exception: Caso ocorra um erro ao remover os dados.
    """
    conn = connect_db(name)
    if conn is None:
        raise Exception("Erro ao conectar ao banco de dados")
    
    try:
        cursor = conn.cursor()
        query = f"DELETE FROM {name} WHERE id = ?"
        cursor.execute(query, (record_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erro ao remover dados: {e}")
    finally:
        conn.close()


def update_data_estoque(name, record_id, qtd_est, qtd_ferramenta, origem, nome_ferram, tempo_uso, tipo):
    """
    Atualiza um registro na tabela cujo nome é o mesmo passado em 'name', baseado no id.
    
    Args:
        name (str): Nome do banco de dados (sem extensão .db) e também nome da tabela.
        record_id (int): ID do registro a ser atualizado.
        qtd_est (int): Nova quantidade de estoque.
        qtd_ferramenta (int): Nova quantidade de ferramentas.
        origem (str): Nova origem.
        nome_ferram (str): Novo nome da ferramenta.
        tempo_uso (int): Novo tempo de uso.
        tipo (str): Novo tipo.
    
    Raises:
        Exception: Caso ocorra um erro ao atualizar os dados.
    """
    conn = connect_db(name)
    if conn is None:
        raise Exception("Erro ao conectar ao banco de dados")
    
    try:
        cursor = conn.cursor()
        query = f"UPDATE {name} SET qtd_est = ?, qtd_ferramenta = ?, origem = ?, nome_ferram = ?, tempo_uso = ?, tipo = ? WHERE id = ?"
        cursor.execute(query, (qtd_est, qtd_ferramenta, origem, nome_ferram, tempo_uso, tipo, record_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erro ao atualizar dados: {e}")
    finally:
        conn.close()
#Função para buscar produtos---------------------------------------------------------------------------------------------------------------------------
def search_product_by_name_estoque(name, product_name):
    """
    Busca um produto na tabela cujo nome é o mesmo passado em 'name', baseado no nome da ferramenta (campo 'nome_ferram').

    Args:
        name (str): Nome do banco de dados (sem extensão .db) e também nome da tabela.
        product_name (str): Nome (ou parte do nome) da ferramenta a ser buscada.

    Returns:
        DataFrame: DataFrame contendo os registros que correspondem ao nome da ferramenta.

    Raises:
        Exception: Caso não seja possível conectar ao banco de dados ou buscar os dados.
    """
    conn = connect_db(name)
    if conn is None:
        raise Exception("Erro ao conectar ao banco de dados")
    
    try:
        query = f"SELECT * FROM {name} WHERE nome_ferram LIKE ?"
        # Utiliza o caractere '%' para permitir buscas parciais
        df = pd.read_sql_query(query, conn, params=(f"%{product_name}%",))
    except Exception as e:
        raise Exception(f"Erro ao buscar o produto '{product_name}': {e}")
    finally:
        conn.close()
    
    return df

#-----------------------------------------MOVIMENTAÇÕES----------------------------------------------------------------------------------------------

def create_db_movimentacao(name):
    """
    Cria o banco de dados e a tabela com os seguintes campos:
    - id: Id único.
    - nome_pessoa: string.
    - matricula: número.
    - data: date.
    - email_solicitante: string.
    - email_gestor: string.
    - movimentacao: TEXT.
    - qtd_mov: inteiro.
    - codigo_ferramenta: inteiro.
    - nome_ferramenta: TEXT.
    
    Args:
        name (str): Nome do banco de dados (sem extensão) e também o nome da tabela a ser criada.
    """
    db_file = f"{name}.db"
    
    # Verifica se o banco de dados já existe
    if os.path.exists(db_file):
        st.write(f"O banco de dados '{db_file}' já existe.")
        return
    
    # Cria a conexão com o banco de dados
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Cria a tabela com os campos especificados
    cursor.execute(f'''
        CREATE TABLE {name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_pessoa TEXT,
            matricula INTEGER,
            data DATE,
            email_solicitante TEXT,
            email_gestor TEXT,
            movimentacao TEXT,
            qtd_mov INTEGER,
            codigo_ferramenta INTEGER,
            nome_ferramenta TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    st.write(f"O banco de dados '{db_file}' e a tabela '{name}' foram criados com sucesso.")

def connect_db(name):
    """
    Conecta ao banco de dados SQLite com o nome especificado.
    
    Args:
        name (str): Nome do banco de dados (sem extensão).
    
    Returns:
        Connection: objeto de conexão com o banco de dados ou None em caso de erro.
    """
    try:
        connection = sqlite3.connect(f'{name}.db', check_same_thread=False)
        return connection
    except sqlite3.Error as e:
        st.write(f"Erro ao conectar ao banco de dados: {e}")
        return None

def insert_data_movimentacao(name, nome_pessoa, matricula, data, email_solicitante, email_gestor, movimentacao, qtd_mov, codigo_ferramenta, nome_ferramenta):
    """
    Insere um novo registro na tabela de movimentacao.
    
    Args:
        name (str): Nome do banco de dados (sem extensão) e também nome da tabela.
        nome_pessoa (str): Nome da pessoa.
        matricula (int): Número da matrícula.
        data (str): Data no formato 'YYYY-MM-DD'.
        email_solicitante (str): Email do solicitante.
        email_gestor (str): Email do gestor.
        movimentacao (str): Tipo de movimentação (texto).
        qtd_mov (int): Quantidade da movimentação.
        codigo_ferramenta (int): Código da ferramenta.
        nome_ferramenta (str): Nome da ferramenta.
    """
    conn = connect_db(name)
    if conn is None:
        st.write("Erro ao conectar ao banco de dados.")
        return
    
    try:
        cursor = conn.cursor()
        query = f"""
            INSERT INTO {name} 
            (nome_pessoa, matricula, data, email_solicitante, email_gestor, movimentacao, qtd_mov, codigo_ferramenta, nome_ferramenta) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (nome_pessoa, matricula, data, email_solicitante, email_gestor, movimentacao, qtd_mov, codigo_ferramenta, nome_ferramenta))
        conn.commit()
        st.write("Registro inserido com sucesso.")
    except Exception as e:
        conn.rollback()
        st.write(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()

def remove_data_movimentacao(name, record_id):
    """
    Remove um registro da tabela de movimentacao baseado no ID.
    
    Args:
        name (str): Nome do banco de dados (sem extensão) e também nome da tabela.
        record_id (int): ID do registro a ser removido.
    """
    conn = connect_db(name)
    if conn is None:
        st.write("Erro ao conectar ao banco de dados.")
        return
    
    try:
        cursor = conn.cursor()
        query = f"DELETE FROM {name} WHERE id = ?"
        cursor.execute(query, (record_id,))
        conn.commit()
        st.write("Registro removido com sucesso.")
    except Exception as e:
        conn.rollback()
        st.write(f"Erro ao remover dados: {e}")
    finally:
        conn.close()

def update_data_movimentacao(name, record_id, nome_pessoa, matricula, data, email_solicitante, email_gestor, movimentacao, qtd_mov, codigo_ferramenta, nome_ferramenta):
    """
    Atualiza um registro na tabela de movimentacao baseado no ID.
    
    Args:
        name (str): Nome do banco de dados (sem extensão) e também nome da tabela.
        record_id (int): ID do registro a ser atualizado.
        nome_pessoa (str): Novo nome da pessoa.
        matricula (int): Nova matrícula.
        data (str): Nova data no formato 'YYYY-MM-DD'.
        email_solicitante (str): Novo email do solicitante.
        email_gestor (str): Novo email do gestor.
        movimentacao (str): Novo tipo de movimentação (texto).
        qtd_mov (int): Nova quantidade de movimentação.
        codigo_ferramenta (int): Novo código da ferramenta.
        nome_ferramenta (str): Novo nome da ferramenta.
    """
    conn = connect_db(name)
    if conn is None:
        st.write("Erro ao conectar ao banco de dados.")
        return
    
    try:
        cursor = conn.cursor()
        query = f"""
            UPDATE {name} 
            SET nome_pessoa = ?, matricula = ?, data = ?, email_solicitante = ?, email_gestor = ?, 
                movimentacao = ?, qtd_mov = ?, codigo_ferramenta = ?, nome_ferramenta = ?
            WHERE id = ?
        """
        cursor.execute(query, (nome_pessoa, matricula, data, email_solicitante, email_gestor, movimentacao, qtd_mov, codigo_ferramenta, nome_ferramenta, record_id))
        conn.commit()
        st.write("Registro atualizado com sucesso.")
    except Exception as e:
        conn.rollback()
        st.write(f"Erro ao atualizar dados: {e}")
    finally:
        conn.close()