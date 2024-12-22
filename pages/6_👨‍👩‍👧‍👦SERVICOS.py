import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="CONSELHO IPSU",
    layout="wide"
)
#st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

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

    function clearLoginState() {
        localStorage.removeItem("logged_in");
    }

    document.addEventListener('DOMContentLoaded', (event) => {
        const loggedIn = getLoginState();
        if (!loggedIn) {
            window.parent.postMessage("logged_out", "*");
        }
    });
</script>
"""

# Incluir o JavaScript no Streamlit
st.components.v1.html(local_storage_script, height=0)

# Função para verificar se o usuário está logado
def is_logged_in():
    return st.session_state.get('logged_in', False)

# Função para limpar o login no localStorage
def logout():
    st.session_state['logged_in'] = False
    st.components.v1.html('<script>clearLoginState();</script>', height=0)

# Verificação de login
if not is_logged_in():
    st.subheader("Você precisa fazer login para acessar este menu")
    st.subheader("Volte para a página inicial")
    st.stop()  # Interrompe o código se não estiver logado

else:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.subheader("Logoff")
    with col2:
        if st.button("Sair"):
            logout()
            st.write("Você foi desconectado")


    path = Path(__file__).parent.parent


    # TÍTULO DA PÁGINA
    st.title("SERVIÇOS E AVALIAÇÃO")

# CARREGAR OS DADOS DA PLANILHA
  
    if "data" in st.session_state:
        df_data = st.session_state["data"]
        df_data = df_data[["Nome completo",
                        "Qual a sua idade?",
                        "Telefone com DDD (preferencialmente whatsapp)",
                        "Em qual ministério você serve?",
                        "Há quanto tempo está na IPSU?",
                        "Em qual sociedade interna você está inserido",
                        "Com base nos tópicos aqui apresentados, houve alguma assunto que não foi abordado e que você gostaria de descrever/expor a respeito?",
                        "Relate-nos",
                        "Você é dizimista?",
                        "Como você avalia o seu conhecimento das Escrituras?"]]

        # Slider para selecionar o intervalo de idades
        
        tempo_ipsu = list(df_data["Há quanto tempo está na IPSU?"].unique())
        dizimista = list(df_data["Você é dizimista?"].unique())
        
                                                                                     
        tempo_ipsu_selecionadas = st.sidebar.multiselect("Selecione o tempo que frequenta a IPSU:", tempo_ipsu, tempo_ipsu)
        dizimista_selecionadas = st.sidebar.multiselect("É dizimista?", dizimista, dizimista)

        st.divider()

        col1, col2 = st.sidebar.columns(2)
        status_filtrar = col1.button("Filtrar")
    
        if status_filtrar:
            df_filtrado = df_data[
                                  (df_data["Há quanto tempo está na IPSU?"].isin(tempo_ipsu_selecionadas)) & 
                                  (df_data["Você é dizimista?"].isin(dizimista_selecionadas))]
        else:
            df_filtrado = df_data

        
        col1, col2 = st.columns([0.8, 0.8])

        with col1:
            status_counts = df_filtrado["Em qual ministério você serve?"].value_counts()
            color_map = {
            "Em qual ministério você serve?": "green",
            "Louvor": "yellow",
            "Sonoplastia": "blue",
            "Mídia": "red",
            "Nenhuma das opções": "purple"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Ministérios", "values":"Avaliação"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Ministérios",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)

        

        with col2:
            status_counts = df_filtrado["Em qual sociedade interna você está inserido"].value_counts()
            color_map = {
            "UPA": "green",
            "UMP": "yellow",
            "SAF": "blue",
            "UPH": "red",
            "Nenhuma das opções": "purple"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Sociedades Internas", "values":"Avaliação"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Sociedades Internas",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)


        st.divider()

        status_counts = df_filtrado["Como você avalia o seu conhecimento das Escrituras?"].value_counts()
        color_map = {
            "0": "yellow",
            "1": "red",
            "2": "green",
            "3": "orange",
            "4": "purple",
            "5": "blue",
            "6": "black",
            "7": "brown",
            "8": "pink",
            "9": "grey",
            "10": "gold"}

        fig = px.pie(
            names=status_counts.index,
            values=status_counts.values,
            labels={"names": "Conhecimento das Escrituras [Média]", "values":"Avaliação"},
            color=status_counts.index,
            color_discrete_map=color_map,
            template="plotly_dark",
            hole=0.3)
            
        fig.update_layout(
            title={
                "text": "Conhecimento das Escrituras",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top"
                }
            )
        st.plotly_chart(fig)

        st.divider()

        status_counts = df_filtrado["Com base nos tópicos aqui apresentados, houve alguma assunto que não foi abordado e que você gostaria de descrever/expor a respeito?"].value_counts()
        color_map = {
            "Sim": "yellow",
            "Não": "red"}

        fig = px.pie(
            names=status_counts.index,
            values=status_counts.values,
            labels={"names": "Com base nos tópicos aqui apresentados, houve alguma assunto que não foi abordado e que você gostaria de descrever/expor a respeito?", "values":"Avaliação"},
            color=status_counts.index,
            color_discrete_map=color_map,
            template="plotly_dark",
            hole=0.3)
            
        fig.update_layout(
            title={
                "text": "Com base nos tópicos aqui apresentados, houve alguma assunto que não foi abordado e que você gostaria de descrever/expor a respeito?",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top"
                }
            )
        st.plotly_chart(fig)
        st.divider()
        st.markdown("Relate-nos")
        df_filtrado["Relate-nos"]
    st.divider()



















    st.dataframe(df_filtrado)

 

    
    st.divider()

    # FUNÇÃO QUE DEFINE A PARA A LOGO
        
    st.sidebar.image("IPSU.png", caption="CONSELHO IPSU")
