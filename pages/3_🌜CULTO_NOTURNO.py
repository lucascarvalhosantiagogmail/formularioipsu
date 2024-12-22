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
    st.title("CULTO NOTURNO")
    
# CARREGAR OS DADOS DA PLANILHA
  
    if "data" in st.session_state:
        df_data = st.session_state["data"]
        df_data = df_data[["Nome completo",
                        "Qual a sua idade?",
                        "Telefone com DDD (preferencialmente whatsapp)",
                        "Há quanto tempo está na IPSU?",
                        "Culto Noturno - Qual seria o horário de início ideal do culto?",
                        "Culto Noturno - Qual seria o horário de término ideal do culto noturno?",
                        "Culto Noturno - Você tem alguma justificativa para a escolha do horário anterior?",
                        "Culto Noturno - Atualmente o nosso culto noturno está composto dos seguintes elementos: Liturgia com Hinos, Louvor, Oração pelo sermão e para o ensino das crianças, Sermão, e avisos após o término...",
                        "Culto Noturno - O que deve ser removido?",
                        "Culto Noturno - O que deve ser inserido?",
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

# HORÁRIO DO CULTO 
        
        col1, col2, col3 = st.columns([0.7,0.7,0.7])

        
        with col1:
            status_counts = df_filtrado["Culto Noturno - Qual seria o horário de início ideal do culto?"].value_counts()
            color_map = {
            "18:00": "green",
            "18:30": "yellow",
            "19:00": "blue",
            "19:30": "purple",
            "20:00": "red"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Horário de Início do Culto Noturno", "values":"Horários"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Horário de Início do Culto Noturno",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)


        with col2:
            status_counts = df_filtrado["Culto Noturno - Qual seria o horário de término ideal do culto noturno?"].value_counts()
            color_map = {
            "19:30": "green",
            "20:00": "yellow",
            "20:30": "blue",
            "21:00": "purple",
            "21:30": "red"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Horário de Término do Culto Noturno", "values":"Horários"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Horário de Término do Culto Noturno",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)
        
                         
        with col3:
            status_counts = df_filtrado["Culto Noturno - Você tem alguma justificativa para a escolha do horário anterior?"].value_counts()
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

# AVALIAÇÃO DO CULTO NOTURNO

        col1, col2, col3 = st.columns([0.8, 0.8, 0.8])

        with col1:
            status_counts = df_filtrado["Culto Noturno - Atualmente o nosso culto noturno está composto dos seguintes elementos: Liturgia com Hinos, Louvor, Oração pelo sermão e para o ensino das crianças, Sermão, e avisos após o término..."]
            color_map={
                "Remoção de algum item": "red",
                "Inserção de algum item": "green",
                "Nada a pontuar": "yellow"}
            
            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Avaliação do Culto Noturno", "values": "Horários"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "Avaliação do Culto Noturno",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)

        with col2:
            status_counts = df_filtrado["Culto Noturno - O que deve ser removido?"]
            color_map={
                "Liturgia com hinos": "red",
                "Louvor": "green",
                "Oração pelo sermão e para o ensino das crianças": "yellow",
                "Sermão": "blue",
                "Avisos": "purple"}
            
            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "O que deve ser removido", "values": "Avaliação"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3)
            
            fig.update_layout(
                title={
                    "text": "O que deve ser removido",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)

        with col3:
            df_filtrado["Culto Noturno - O que deve ser inserido?"]
           
    st.divider()
    st.dataframe(df_filtrado)

    # FUNÇÃO QUE DEFINE A PARA A LOGO
        
    st.sidebar.image("IPSU.png", caption="CONSELHO IPSU")
 