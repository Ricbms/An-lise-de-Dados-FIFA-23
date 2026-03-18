import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jogadores",page_icon="🙅‍♂️",layout="wide")
#Carregando os dados
df_data = st.session_state['data']

#Criando a sidebar com filtro por time e jogador
times = df_data['Club'].value_counts().index
time_side = st.sidebar.selectbox("Time", times)

df_jogadores = df_data[(df_data["Club"] == time_side)]

jogadores = df_jogadores['Name'].value_counts().index
jogador = st.sidebar.selectbox("Jogador", jogadores)
st.sidebar.markdown('🔗 Desenvolvido por [Richard Silva](https://www.linkedin.com/in/richard-silva-555887195/)')

#Criando visualização da pagina jogadores

estatistica = df_jogadores[df_jogadores['Name'] == jogador].iloc[0]


esquerda, centro, direita = st.columns([1, 4, 1])

with centro:
    st.markdown(
        f'<img src="{estatistica["Photo"]}" width="60" referrerpolicy="no-referrer">',
        unsafe_allow_html=True
    )
    # Nome do jogador
    st.title(estatistica["Name"])

    st.markdown(f"**Clube:** {estatistica['Club']}")
    st.markdown(f"**Posição:** {estatistica['Position']}")
    #Aula 1358

    col1, col2, col3, col4 = st.columns(4)

    # col1.markdown(f"**Idade:** {estatistica['Age']}")
    # col2.markdown(f"**Altura:** {estatistica['Height(cm.)']/100} cm")
    # col3.markdown(f"**Peso:** {estatistica['Weight(lbs.)']*0.453:.2f} kg")

    col1.metric("Idade", estatistica['Age'])
    col2.metric("Altura", f"{estatistica['Height(cm.)']/100:.2f} m")
    col3.metric("Peso", f"{estatistica['Weight(lbs.)']*0.453:.2f} kg")
    st.divider()


    st.subheader(f"Overall: {estatistica["Overall"]}")
    st.markdown("""
        <style>
        .stProgress > div > div > div > div {
            background-color: red;
        }
        </style>
    """, unsafe_allow_html=True)
    st.progress(int(estatistica["Overall"]))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Valor", value=f"{estatistica['Value(£)']:,}")
    col2.metric(label="Remuneração", value=f"{estatistica['Wage(£)']:,}")
    col3.metric(label="Valor de rescisão", value=f"{estatistica['Release Clause(£)']:,}")