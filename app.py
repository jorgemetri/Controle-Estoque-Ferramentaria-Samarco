import streamlit as st
import os

# Configurações da página
st.set_page_config(
    page_title="Sistema de Controle de Estoque",
    page_icon=":bar_chart:",
    layout="wide"  # Define o layout como "wide"
)

# Função para exibir o logo
def Logo(url):
    st.logo(
        url,
        link="https://streamlit.io/gallery", size="large"
    )

LOGO_URL_LARGE = "images/samarco.png"  # Substitua pelo caminho da sua logo
Logo(LOGO_URL_LARGE)

# Função para sair da aplicação
def logout():
    st.session_state.logged_in = False
    st.success("Você saiu da aplicação com sucesso!")
    st.rerun()  # Recarrega a aplicação para voltar à tela de login

# Verifica se o usuário está logado
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Se o usuário estiver logado, exibe o botão de sair
if st.session_state.logged_in:
    if st.sidebar.button("Sair"):
        logout()

# Navegação e páginas
if st.session_state.logged_in:
    # Páginas para Ferramentas de Estoque
    cadastrar = st.Page("ferramentas_estoque/cadastrar.py", title="Cadastrar Produto", icon=":material/add:")
    entradasaida = st.Page("ferramentas_estoque/entradasaida.py", title="Entrada/Saída", icon=":material/swap_horiz:")
    buscarproduto = st.Page("ferramentas_estoque/buscarproduto.py", title="Buscar Produto", icon=":material/search:")
    visualizarestoque = st.Page("ferramentas_estoque/visualizarestoque.py", title="Visualizar Estoque", icon=":material/list:")
    movimentacoes = st.Page("ferramentas_estoque/movimentacoes.py", title="Movimentações", icon=":material/trending_up:")

    # Páginas para Indicadores de Estoque
    graficoestoque = st.Page("indicadores_estoque/graficoestoque.py", title="Gráficos de Estoque", icon=":material/bar_chart:")

    # Páginas para Previsão de Estoque
    previsao = st.Page("previsao_estoque/previsao.py", title="Previsão de Estoque", icon=":material/timeline:")

    # Navegação
    pg = st.navigation(
        {
            "Ferramentas de Estoque": [cadastrar, entradasaida, buscarproduto, visualizarestoque, movimentacoes],
            "Indicadores de Estoque": [graficoestoque],
            "Previsão de Estoque": [previsao]
        }
    )
    pg.run()
else:
    # Tela de login
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":  # Simulação de login
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
            st.rerun()  # Recarrega a aplicação para exibir as páginas
        else:
            st.error("Usuário ou senha incorretos.")