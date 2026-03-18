import streamlit as st
import pandas as pd

# Configuração da página (deve ser a primeira coisa no script)
st.set_page_config(
    page_title="FIFA Data Analysis",
    page_icon="⚽",
    layout="wide"
)

st.title("🏆 Bem-vindo ao Dashboard FIFA 2023")

st.markdown("""
Este dashboard foi desenvolvido durante o curso da **Asimov Academy**, 
com incrementos e melhorias adicionais implementados ao longo do aprendizado.

---

### 📌 O que você encontra aqui:

- ⚽ **Times** — Explore os elencos dos clubes, com estatísticas detalhadas de cada jogador
- 👤 **Jogadores** — Visualize o perfil completo de cada atleta, incluindo foto, overall e métricas físicas  
- 📊 **Análise** — Gráficos e insights sobre os dados do FIFA 23, com visualizações customizadas

---

### 🚀 Como usar:
Utilize o **menu lateral** para navegar entre as seções e os filtros disponíveis em cada página.

---

*Dados baseados no dataset FIFA 23 | Projeto desenvolvido com Python, Streamlit, Pandas e Plotly*
""")

st.sidebar.markdown('🔗 Desenvolvido por [Richard Silva](https://www.linkedin.com/in/richard-silva-555887195/)')



if "data" not in st.session_state:
    df_data = pd.read_csv("CLEAN_FIFA23_official_data.csv", index_col=0)
    df_data = df_data.sort_values("Overall", ascending=False)
    st.session_state["data"] = df_data




st.divider()

st.subheader("📂 Fonte dos Dados")

st.markdown(
"Dataset disponível no Kaggle: "
"https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data"
)

with st.expander("Visualizar dataset"):
    st.write(st.session_state["data"])