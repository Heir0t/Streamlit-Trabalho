import streamlit as st
import plotly.express as px
from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title='Visao Geral',
    layout='wide'
)

st.title('Visao Geral do Dataset')

df = carregar_dados()

if df.empty:
    st.stop()

with st.expander("Filtros de Dados", expanded=True):
    col_genero, col_explicit = st.columns([3, 1])
    
    todos_generos = sorted(df['track_genre'].unique())
    top_10_padrao = df['track_genre'].value_counts().head(10).index.tolist()

    with col_genero:
        filtro_generos = st.multiselect(
            "Selecione os Generos",
            options=todos_generos,
            default=top_10_padrao,
            help="Filtre os dados por categoria musical"
        )

    with col_explicit:
        filtro_explicit = st.selectbox(
            "Conteudo Explicito",
            options=["Todos", "Sim", "Nao"],
            index=0
        )

    filtro_pop = st.slider(
        "Faixa de Popularidade",
        min_value=0,
        max_value=100,
        value=(0, 100)
    )

df_filtrado = df.copy()

if filtro_generos:
    df_filtrado = df_filtrado[df_filtrado['track_genre'].isin(filtro_generos)]
else:
    st.warning("Selecione pelo menos um genero para visualizar os dados")
    st.stop()

if filtro_explicit != "Todos":
    valor_para_filtrar = "Explicito" if filtro_explicit == "Sim" else "Nao Explicito"
    df_filtrado = df_filtrado[df_filtrado['explicit_str'] == valor_para_filtrar]

df_filtrado = df_filtrado[
    (df_filtrado['popularity'] >= filtro_pop[0]) &
    (df_filtrado['popularity'] <= filtro_pop[1])
]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com essa combinacao de filtros")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Faixas", len(df_filtrado))
col2.metric("Artistas Unicos", df_filtrado['artists'].nunique())
col3.metric("Generos Selecionados", df_filtrado['track_genre'].nunique())
col4.metric("Duracao Media (min)", f"{df_filtrado['duration_min'].mean():.2f}")

st.divider()

st.subheader('Distribuicao de Popularidade por Genero Selecionado')

fig = px.box(df_filtrado,
    x='track_genre',
    y='popularity',
    points='outliers', 
    title=f'Distribuicao de Popularidade ({len(df_filtrado)} faixas)',
    labels={'popularity':'Popularidade (0-100)', 'track_genre':'Genero'},
    color='track_genre'
)

fig.update_layout(
    xaxis_title_text='Genero Musical',
    yaxis_title_text='Popularidade',
    title_x=0.5,
    margin=dict(t=80),
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader('Relacao Energia vs Conteudo Explicito')

fig_energy = px.box(df_filtrado,
    x='explicit_str',
    y='energy',
    points='outliers',
    title='Energia: Musicas Explicitas vs Nao Explicitas',
    labels={'energy':'Energia (0-1)', 'explicit_str':'Conteudo Explicito'},
    color='explicit_str',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_energy.update_layout(
    xaxis_title_text='Classificacao',
    yaxis_title_text='Nivel de Energia',
    title_x=0.5,
    margin=dict(t=80)
)
st.plotly_chart(fig_energy, use_container_width=True)

st.divider()

st.subheader('Proporcao de Conteudo Explicito na Selecao')

df_explicit_pie = (
    df_filtrado['explicit_str']
    .value_counts(normalize=True)
    .reset_index()
    .rename(columns={'explicit_str': 'tipo', 'proportion': 'percentual'})
)

if not df_explicit_pie.empty:
    fig_donut = px.pie(
        df_explicit_pie,
        values='percentual',
        names='tipo',
        hole=0.5,
        title='Divisao: Explicito vs Limpo',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_donut.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)
else:
    st.info("Dados insuficientes para gerar o grafico de pizza")