import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analise",page_icon="‍📈",layout="wide")

df_data = st.session_state['data']


times = df_data['Club'].value_counts().index
time_side = st.sidebar.selectbox("Time", times)

st.sidebar.markdown('🔗 Desenvolvido por [Richard Silva](https://www.linkedin.com/in/richard-silva-555887195/)')

df_clubes = df_data[(df_data["Club"] == time_side)].set_index("Name")

esquerda, centro, direita = st.columns([1, 4, 1])

with centro:
    st.title("⚽ Análise Exploratória dos Dados")

    #### GRAFICOS ##########
    st.subheader(f"Resumo: {time_side}")

    df_clubes["Wage_Num"] = pd.to_numeric(df_clubes["Wage(£)"].astype(str).str.replace('£', '').str.replace(',', ''),
                                          errors='coerce').fillna(0)

    # Cálculo de métricas
    media_overall = df_clubes["Overall"].mean()
    media_potencial = df_clubes["Potential"].mean()
    media_idade = df_clubes["Age"].mean()
    media_salario = df_clubes["Wage_Num"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Média de Overall", f"{media_overall:.1f}")
    col2.metric("Média de Potencial", f"{media_potencial:.1f}")
    col3.metric("Média de Idade", f"{media_idade:.0f} anos")
    col4.metric("Média de Salário (Semana)", f"£ {media_salario:,.2f}")

    st.divider()

    #### GRAFICO 1 Dispersão entre idade e Overall ##########
    st.subheader("Comparação entre Experiência e Avaliação")

    fig_idade = px.scatter(
        df_clubes.reset_index(),
        x="Age",
        y="Overall",
        hover_name="Name",
        size="Overall",
        color="Potential",
        title=f"Jogadores do {time_side}: Idade vs Overall",
        color_continuous_scale="greens",
        labels={"Age": "Idade", "Overall": "Nível Atual", "Potential": "Potencial Futuro"}
    )
    st.plotly_chart(fig_idade, use_container_width=True)

    st.write("""
     **Análise:** Jogadores no canto superior esquerdo são considerados Promessas (jovens e bons). 
    No canto superior direito estão os 'Veteranos de Elite'.
    """)

    st.divider()

    #### GRAFICO 2 Overall time ##########

    st.subheader(f"🔝 Top 10 Jogadores: {time_side}")

    top_10_players = df_clubes.sort_values("Overall", ascending=False).head(10).reset_index()

    fig_top10 = px.bar(
        top_10_players,
        x="Overall",
        y="Name",
        orientation='h',
        text="Overall",   # Mostra o valor em cima da barra
        title=f"Líderes de Performance - {time_side}",
        color="Overall",
        color_continuous_scale="greens",
        labels={"Name": "", "Overall": "Nível"},
        template="plotly_dark"
    )

    #COLOCANDO EM ORDEM
    fig_top10.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig_top10, use_container_width=True)

    st.divider()


    ### GRAFICO 3  POTENCIAL X OVERALL ATUAL####

    st.subheader("Análise de Crescimento por Posição")

    # Criamos um resumo por posição
    df_posicao = df_clubes.groupby("Position")[["Overall", "Potential"]].mean().reset_index()

    df_melted = df_posicao.melt(id_vars="Position", var_name="Tipo", value_name="Nível")

    fig_crescimento = px.bar(
        df_melted,
        x="Position",
        y="Nível",
        color="Tipo",
        barmode="group",  # Coloca as barras lado a lado
        title="Diferença entre Nível Atual e Potencial por Setor",
        color_discrete_map={"Overall": "#53E069", "Potential": "#E1322F"},
        template="plotly_dark",
        labels={"Nível": "", "Position": "Posição em Campo (Inglês)"},
    )

    st.plotly_chart(fig_crescimento, use_container_width=True)

    st.write("""
    **Análise:** Quanto maior a distância entre a barra de Potencial e Overall, 
    mais jovens talentos o time possui nessa posição específica.
    """)

    st.divider()


    #### GRAFICO 4 ######

    st.subheader("💰 Maiores Salários")
    top_salarios = df_clubes.sort_values("Wage_Num", ascending=False).head(10).reset_index()
    fig_salarios = px.bar(
        top_salarios, x="Wage_Num",
        y="Name",
        orientation='h',
        color="Wage_Num",
        color_continuous_scale="Greens",
        template="plotly_dark",
        labels={"Wage_Num": "Salário (£)","Name":""}
    )
    fig_salarios.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    st.plotly_chart(fig_salarios, use_container_width=True)

    st.divider()

    #### GRAFICO 5 ######


    st.subheader("📊 Nível do Elenco")
    fig_dist = px.histogram(
        df_clubes, x="Overall", nbins=10,
        title="Frequência de Qualidade", color_discrete_sequence=['#2ecc71'],
        template="plotly_dark"
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    st.write("""
    **Análise:** Grafico de distribuição baseado na qualidade do elenco, quanto maior a barra maior
    a barra, maior a quantidade de jogadores naquele nível.
    """)

    st.divider()

    #### GRAFICO 6 ######

    st.subheader("📏 Perfil de Altura")
    fig_height = px.box(
        df_clubes, y="Height(cm.)",
        points="all", title="Distribuição de Altura (cm)",
        color_discrete_sequence=['#27ae60'], template="plotly_dark"
    )
    st.plotly_chart(fig_height, use_container_width=True)

    st.info("""
        **Como ler o Boxplot?**
        A linha central na caixa verde indica a **mediana** de altura. 
        A 'caixa' concentra os 50% dos jogadores com altura mais comum no elenco. 
        Pontos muito distantes representam os jogadores com altura fora do padrão (os mais altos ou mais baixos).
        """)

    st.divider()

    #### GRAFICO 7 ######

    st.subheader("🦶 Lateralidade")
    fig_foot = px.pie(
        df_clubes, names="Preferred Foot", hole=0.5,
        color="Preferred Foot",
        color_discrete_map={"Right": "#53E069", "Left": "#E1322F"},
        template="plotly_dark",
        title="Os jogadores nesse time usam principalmante o pé direito ou esquerdo? ",
    )
    st.plotly_chart(fig_foot, use_container_width=True)

    st.divider()
#---------------------------------------------------------

    #### Ultimo gafico #########

    st.subheader("🌍 Origem do Plantel (Scouting Mundial)")

    # Contagem de jogadores por nacionalidade no clube
    nacionalidades = df_clubes["Nationality"].value_counts().reset_index()
    nacionalidades.columns = ["Nationality", "Contagem"]

    fig_mapa = px.choropleth(
        nacionalidades,
        locations="Nationality",
        locationmode="country names",
        color="Contagem",
        hover_name="Nationality",
        title=f"Distribuição Geográfica: {time_side}",
        color_continuous_scale="Greens",
        template="plotly_dark"
    )

    fig_mapa.update_geos(
        showcoastlines=True,
        coastlinecolor="DarkGreen",
        showland=True,
        landcolor="#1e1e1e",
        showocean=True,
        oceancolor="#0e1117"  # Cor de fundo padrão do Streamlit Dark
    )

    fig_mapa.update_layout(
        height=700,  # Aumenta a altura significativamente
        margin={"r": 0, "t": 50, "l": 0, "b": 0}  # Remove as margens brancas laterais
    )

    st.plotly_chart(fig_mapa, use_container_width=True)

    st.info("""
        Regiões escuras dizem que o elenco não conta com jogadores daqueles país.
        """)

    st.divider()