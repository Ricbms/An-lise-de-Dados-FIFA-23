import streamlit as st
import pandas as pd

st.set_page_config(page_title="Times",page_icon="‍💒️",layout="wide")

df_data = st.session_state['data']

times = df_data['Club'].value_counts().index
time_side = st.sidebar.selectbox("Time", times)

st.sidebar.markdown('🔗 Desenvolvido por [Richard Silva](https://www.linkedin.com/in/richard-silva-555887195/)')

df_clubes = df_data[(df_data["Club"] == time_side)].set_index("Name")



esquerda, centro, direita = st.columns([1, 4, 1])

with centro:
    st.markdown(
        f'<img src="{df_clubes.iloc[0]["Club Logo"]}" width="45" referrerpolicy="no-referrer">',
        unsafe_allow_html=True
    )
    # Nome do time
    st.markdown(f"## {time_side}")
    st.divider()

    colunas_sl = ["Age","Nationality","Photo","Flag","Overall","Value(£)","Wage(£)","Joined","Height(cm.)","Year_Joined"]


    #corrindo erro das imagens
    df_clubes["Photo"] = df_clubes["Photo"].apply(
        lambda url: f"https://images.weserv.nl/?url={url}"
    )
    df_clubes["Flag"] = df_clubes["Flag"].apply(
        lambda url: f"https://images.weserv.nl/?url={url}"
    )

    #tabela e configurações da tabela
    st.dataframe(df_clubes[colunas_sl],
                 column_config={
                     "Overall": st.column_config.ProgressColumn(
                         "Overall", min_value=0,max_value=100,format="%d"),
                     "Wage(£)": st.column_config.ProgressColumn(
                        "Wage(£)",format="%f",min_value=0,max_value=df_clubes['Wage(£)'].max()),
                     "Photo": st.column_config.ImageColumn(),
                     "Flag": st.column_config.ImageColumn(),
                     "Value(£)": st.column_config.NumberColumn(
                         "Value(£)", format="£ %.2f", step=0.01),
                 })