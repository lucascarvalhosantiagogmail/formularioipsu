import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path



path = Path(__file__).parent


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Conselho IPSU",
    #page_icon= "https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
    layout="wide")
st.markdown("Esta página é para visualização das informações oriundas do Formulário - Visão 2025 - IPSU"
            "Serão apresentadas de modo gráfico, para que se tenha uma melhor avaliação das métricas")
# Atualização da página a cada 5 minutos. Não permitir a hibernação.
keep_alive_script = """
<script>
    function keepAlive() {
        setInterval(function() {
            console.log("Sending keep-alive ping...");
            fetch("/").then(response => {
                console.log("Ping response: ", response);
            });
        }, 300000); // A cada 5 minutos
    }
    document.addEventListener('DOMContentLoaded', keepAlive);
</script>
"""

st.components.v1.html(keep_alive_script, height=0)

# Função JavaScript para manipular o localStorage
local_storage_script = """
<script>
    function getLoginState() {
        return localStorage.getItem("logged_in") === "true";
    }

    function setLoginState(value) {
        localStorage.setItem("logged_in", value);
    }

    function clearLoginState() {
        localStorage.removeItem("logged_in");
    }

    // Atualiza o estado de login ao carregar a página
    document.addEventListener('DOMContentLoaded', (event) => {
        const loggedIn = getLoginState();
        window.parent.postMessage(loggedIn ? 'logged_in' : 'logged_out', '*');
    });
</script>
"""

# Incluir o JavaScript no Streamlit
st.components.v1.html(local_storage_script, height=0)

# Função para verificar se o usuário está logado no localStorage (JavaScript)
def check_login_state():
    return st.session_state.get('logged_in', False)

# Função para salvar o login no localStorage
def login():
    st.session_state['logged_in'] = True
    st.components.v1.html('<script>setLoginState(true);</script>', height=0)

# Função para limpar o login no localStorage
def logout():
    st.session_state['logged_in'] = False
    st.components.v1.html('<script>clearLoginState();</script>', height=0)

# Verificar estado de login ao carregar a página
if not check_login_state():
    # Verificar o estado no JavaScript (executado ao recarregar)
    st.components.v1.html('<script>if (getLoginState()) { window.parent.postMessage("logged_in", "*"); } else { window.parent.postMessage("logged_out", "*"); }</script>', height=0)


# CARREGAR OS DADOS DA PLANILHA

if "data" not in st.session_state:
    all_sheets = pd.read_excel(path / "dataset"/ "IPSU.xlsx", sheet_name=None)
    df_data = pd.concat(all_sheets.values(), ignore_index=True, join="outer")
    df_data["Hora de início"] = pd.to_datetime(df_data["Hora de início"])
    df_data["Hora de conclusão"] = pd.to_datetime(df_data["Hora de conclusão"])
    df_data["Qual a sua idade?"] = pd.to_numeric(df_data["Qual a sua idade?"])
    df_data["Como você avalia o seu conhecimento das Escrituras?"] = pd.to_numeric(df_data["Como você avalia o seu conhecimento das Escrituras?"])
    st.session_state["data"] = df_data
    
else:
    df_data = st.session_state["data"]

# Verificar estado de login
if check_login_state():
    # LOGO
    st.sidebar.image("IPSU.png", caption="CONSELHO IPSU")

    # TÍTULO
    st.title("CONSELHO IPSU")
    #st.image("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg=true,m/cr=w:134,h:100/qt=q:100/ll")

    st.divider()

    # TEXTO
    st.header("Seja bem-vindo!")

    if st.button("Logout"):
        logout()
        st.write("Você foi deslogado. Recarregue a página para realizar o login novamente.")
else:
    st.sidebar.image("IPSU.png", caption="CONSELHO IPSU")
    #st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")
    st.title("CONSELHO IPSU")
    st.header("Seja bem-vindo!")
    st.subheader("Para acesso as informações, informe a senha.")
    st.divider()

    # Formulário de Login
    st.subheader("Senha de acesso:")
    #login_input = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if password == "nobiscumDeus":
            login()
            st.markdown(
                """
                <div style='text-align: center;'>
                    <h2 style='color: green;'>Página liberada para acesso. Clique nos menus laterais para acessar.</h2>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.error("E-mail ou senha incorretos. Tente novamente.")

st.divider()
#st.subheader("Entre com o seguinte login:")
#st.subheader("E-mail: teste@teste.com.br")
#st.subheader("Senha: 123456")
#st.sidebar.markdown("Desenvolvido por Santiago Engenharia (https://santiagoengenharia.com)")