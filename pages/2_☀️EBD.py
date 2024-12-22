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
    st.title("ESCOLA BÍBLICA DOMINICAL")
    #st.header("Empresa: Engenharia LTDA")
    #st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

# CARREGAR OS DADOS DA PLANILHA
  
    if "data" in st.session_state:
        df_data = st.session_state["data"]
        df_data = df_data[["Nome completo",
                        "Qual a sua idade?",
                        "Telefone com DDD (preferencialmente whatsapp)",
                        "Há quanto tempo está na IPSU?",
                        "EBD - Qual seria o horário de início ideal da?",
                        "EBD - Qual seria o horário de término ideal?",
                        "EBD - Você tem alguma justificativa para a escolha do horário anterior?",
                        "EBD - Atualmente a nossa EBD está composta dos seguintes elementos: Devocional, Louvor, Aniversariantes e Avisos, Aula. Há alguma sugestão/crítica relacionada à algum destes elementos?",
                        "EBD - O que deve ser removido?",
                        "EBD - O que deve ser inserido?",
                        "Você é dizimista?",
                        "Como você avalia o seu conhecimento das Escrituras?"]]
           
        # FILTROS

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

        st.divider()

     # EBD - HORÁRIO   
        col1, col2, col3 = st.columns([0.7, 0.7, 0.7])
       
        with col1:
            status_counts = df_filtrado["EBD - Qual seria o horário de início ideal da?"].value_counts()
            color_map = {
            "08:00": "green",
            "08:30": "yellow",
            "09:00": "blue",
            "09:30": "purple",
            "10:00": "red",
            "10:30": "orange"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Horário de Início da EBD", "values":"Horários"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Horário de Início da EBD",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)


        with col2:
            status_counts = df_filtrado["EBD - Qual seria o horário de término ideal?"].value_counts()
            color_map = {
            "09:00": "green",
            "09:30": "yellow",
            "10:00": "blue",
            "10:30": "purple",
            "11:00": "red",
            "11:30": "orange"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Horário de Término da EBD", "values":"Horários"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Horário de Término da EBD",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)
        
                         
        with col3:
            status_counts = df_filtrado["EBD - Você tem alguma justificativa para a escolha do horário anterior?"].value_counts()
            color_map = {
            "Preferência pessoal": "green",
            "Tempo de deslocamento": "yellow",
            "Compromissos pessoais/familiares antes/após nossa reunião": "blue",
            "Outros": "purple"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Justificativa da Escolha do Horário", "values":"Horários"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Justificativa da Escolha do Horário",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)

        st.divider()      

# EBD - AVALIAÇÃO

        col1, col2, col3 = st.columns([0.7, 0.7, 0.7])
       
        with col1:
            status_counts = df_filtrado["EBD - Atualmente a nossa EBD está composta dos seguintes elementos: Devocional, Louvor, Aniversariantes e Avisos, Aula. Há alguma sugestão/crítica relacionada à algum destes elementos?"].value_counts()
            color_map = {
            "Remoção de algum item": "red",
            "Inserção de algum item": "green",
            "Nada a pontuar": "yellow"}       
                       
            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Avaliação da EBD", "values":"Avaliação"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Avaliação da EBD",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)


        with col2:
            status_counts = df_filtrado["EBD - O que deve ser removido?"].value_counts()
            color_map = {
            "Remoção de algum item": "red",
            "Inserção de algum item": "green",
            "Nada a pontuar": "yellow"}       
                       
            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "O que deve ser removido da EBD", "values":"Avaliação"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "O que deve ser removido da EBD",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)


        with col3:
            status_counts = df_filtrado["EBD - O que deve ser inserido?"].value_counts()
            color_map = {
            "Remoção de algum item": "red",
            "Inserção de algum item": "green",
            "Nada a pontuar": "yellow"}       
                       
            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "O que deve ser inserido na EBD", "values":"Avaliação"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "O que deve ser inserido na EBD",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)

    st.divider()
    st.dataframe(df_filtrado)


    # FUNÇÃO QUE DEFINE A PARA A LOGO
        
    st.sidebar.image("IPSU.png", caption="CONSELHO IPSU")
    