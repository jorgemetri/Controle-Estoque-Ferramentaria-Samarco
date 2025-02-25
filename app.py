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

# Inicializa a sessão de login, se ainda não existir
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Se o usuário não estiver logado, injeta CSS para ocultar a sidebar
if not st.session_state.logged_in:
    hide_sidebar_style = """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Se o usuário estiver logado, exibe a sidebar com o botão de sair e a navegação
if st.session_state.logged_in:
    with st.sidebar:
        if st.button("Sair"):
            logout()

    # Páginas para Ferramentas de Estoque
    cadastrar = st.Page("ferramentas_estoque/cadastrar.py", title="Cadastrar Produto", icon=":material/add:")
    entradasaida = st.Page("ferramentas_estoque/entradasaida.py", title="Entrada/Saída", icon=":material/swap_horiz:")
    buscarproduto = st.Page("ferramentas_estoque/buscarproduto.py", title="Buscar Produto", icon=":material/search:")
    visualizarestoque = st.Page("ferramentas_estoque/visualizarestoque.py", title="Visualizar Estoque", icon=":material/list:")
    movimentacoes = st.Page("ferramentas_estoque/movimentacoes.py", title="Movimentações", icon=":material/trending_up:")
    teste = st.Page("ferramentas_estoque/teste.py",title="Teste")
    # Página para Indicadores de Estoque
    graficoestoque = st.Page("indicadores_estoque/graficoestoque.py", title="Gráficos de Estoque", icon=":material/bar_chart:")

    # Página para Previsão de Estoque
    previsao = st.Page("previsao_estoque/previsao.py", title="Previsão de Estoque", icon=":material/timeline:")

    # Navegação
    pg = st.navigation(
        {
            "Ferramentas de Estoque": [cadastrar, entradasaida, buscarproduto, visualizarestoque, movimentacoes,teste],
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
