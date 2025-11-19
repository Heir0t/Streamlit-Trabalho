import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.carrega_dados import carregar_dados
import pandas as pd

st.set_page_config(
    page_title='Análise Musical',
    layout='wide'
)

st.title('🎵 Análise de Características Musicais')

df = carregar_dados()

if df.empty:
    st.stop()

# Sidebar com filtros
with st.sidebar:
    st.header("Filtros")
    
    # Filtro de gênero
    generos_selecionados = st.multiselect(
        "Gêneros",
        options=sorted(df['track_genre'].unique()),
        default=df['track_genre'].value_counts().head(5).index.tolist()
    )
    
    # Filtro de ano (se existir coluna de ano/data)
    st.divider()
    
    # Filtro de características musicais
    st.subheader("Faixa de Características")
    
    col1, col2 = st.columns(2)
    with col1:
        min_danceability = st.slider(
            "Dançabilidade mínima",
            0.0, 1.0, 0.0, 0.1
        )
    with col2:
        min_energy = st.slider(
            "Energia mínima",
            0.0, 1.0, 0.0, 0.1
        )

# Aplicar filtros
df_filtrado = df.copy()

if generos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['track_genre'].isin(generos_selecionados)]
else:
    st.warning("⚠️ Selecione pelo menos um gênero")
    st.stop()

df_filtrado = df_filtrado[
    (df_filtrado['danceability'] >= min_danceability) &
    (df_filtrado['energy'] >= min_energy)
]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com esses filtros")
    st.stop()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faixas Analisadas", len(df_filtrado))
col2.metric("Dançabilidade Média", f"{df_filtrado['danceability'].mean():.2f}")
col3.metric("Energia Média", f"{df_filtrado['energy'].mean():.2f}")
col4.metric("Valência Média", f"{df_filtrado['valence'].mean():.2f}")

st.divider()

# Gráfico 1: Scatter Plot Interativo - Dançabilidade vs Energia
st.subheader("📊 Relação entre Dançabilidade e Energia")

fig_scatter = px.scatter(
    df_filtrado.sample(min(1000, len(df_filtrado))),  # Limitar para performance
    x='danceability',
    y='energy',
    color='track_genre',
    size='popularity',
    hover_data=['track_name', 'artists', 'popularity'],
    title='Dançabilidade vs Energia (tamanho = popularidade)',
    labels={
        'danceability': 'Dançabilidade (0-1)',
        'energy': 'Energia (0-1)',
        'track_genre': 'Gênero'
    },
    opacity=0.6
)

fig_scatter.update_layout(
    height=500,
    title_x=0.5,
    hovermode='closest'
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# Gráfico 2: Radar Chart - Perfil Musical por Gênero
st.subheader("🎯 Perfil Musical Médio por Gênero")

# Selecionar características para o radar
caracteristicas = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']

# Calcular médias por gênero
df_radar = df_filtrado.groupby('track_genre')[caracteristicas].mean().reset_index()

# Criar radar chart
fig_radar = go.Figure()

for idx, row in df_radar.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=[row[c] for c in caracteristicas],
        theta=[c.capitalize() for c in caracteristicas],
        fill='toself',
        name=row['track_genre'],
        opacity=0.6
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )
    ),
    showlegend=True,
    title="Comparação de Características Musicais",
    title_x=0.5,
    height=500
)
st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# Gráfico 3: Heatmap de Correlação
st.subheader("🔥 Mapa de Calor - Correlação entre Características")

col_corr1, col_corr2 = st.columns([2, 1])

with col_corr1:
    # Características para correlação
    caracteristicas_corr = ['danceability', 'energy', 'valence', 'acousticness', 
                            'instrumentalness', 'speechiness', 'liveness', 'popularity']
    
    # Calcular correlação
    corr_matrix = df_filtrado[caracteristicas_corr].corr()
    
    fig_heatmap = px.imshow(
        corr_matrix,
        labels=dict(color="Correlação"),
        x=[c.capitalize() for c in caracteristicas_corr],
        y=[c.capitalize() for c in caracteristicas_corr],
        color_continuous_scale='RdBu_r',
        aspect="auto",
        zmin=-1,
        zmax=1
    )
    
    fig_heatmap.update_layout(
        title="Correlação entre Atributos Musicais",
        title_x=0.5,
        height=500
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col_corr2:
    st.info("""
    **Como interpretar:**
    
    🔴 **Vermelho intenso**: Correlação positiva forte
    
    🔵 **Azul intenso**: Correlação negativa forte
    
    ⚪ **Branco**: Sem correlação
    
    Correlações próximas de ±1 indicam relação forte entre as características.
    """)

st.divider()

# Gráfico 4: Violin Plot - Distribuição de Valência por Gênero
st.subheader("🎻 Distribuição de Valência Musical")

fig_violin = px.violin(
    df_filtrado,
    x='track_genre',
    y='valence',
    color='track_genre',
    box=True,
    points='outliers',
    title='Valência por Gênero (com outliers)',
    labels={
        'valence': 'Valência (0=triste, 1=feliz)',
        'track_genre': 'Gênero'
    }
)

fig_violin.update_layout(
    height=500,
    title_x=0.5,
    showlegend=False,
    xaxis_title="Gênero Musical",
    yaxis_title="Valência (Positividade)"
)
st.plotly_chart(fig_violin, use_container_width=True)

st.divider()

# Informações adicionais
with st.expander("ℹ️ Sobre as Características Musicais"):
    st.markdown("""
    ### Glossário de Atributos Musicais
    
    - **Dançabilidade**: Quão adequada a música é para dançar (0 = não dançante, 1 = muito dançante)
    - **Energia**: Intensidade e atividade percebida (0 = calma, 1 = energética)
    - **Valência**: Positividade da música (0 = triste/negativa, 1 = feliz/positiva)
    - **Acusticidade**: Probabilidade da música ser acústica (0 = elétrica, 1 = acústica)
    - **Instrumentalidade**: Ausência de vocais (0 = muito vocal, 1 = instrumental)
    - **Speechiness**: Presença de palavras faladas (0 = música, 1 = podcast/spoken word)
    - **Liveness**: Probabilidade de ser gravação ao vivo (0 = estúdio, 1 = ao vivo)
    """)

# Análise textual
st.subheader("📈 Insights da Análise")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    genero_mais_dancavel = df_filtrado.groupby('track_genre')['danceability'].mean().idxmax()
    valor_dancavel = df_filtrado.groupby('track_genre')['danceability'].mean().max()
    st.success(f"**Gênero mais dançante:** {genero_mais_dancavel} ({valor_dancavel:.2f})")
    
    genero_mais_energetico = df_filtrado.groupby('track_genre')['energy'].mean().idxmax()
    valor_energia = df_filtrado.groupby('track_genre')['energy'].mean().max()
    st.info(f"**Gênero mais energético:** {genero_mais_energetico} ({valor_energia:.2f})")

with col_insight2:
    genero_mais_positivo = df_filtrado.groupby('track_genre')['valence'].mean().idxmax()
    valor_valence = df_filtrado.groupby('track_genre')['valence'].mean().max()
    st.success(f"**Gênero mais positivo:** {genero_mais_positivo} ({valor_valence:.2f})")
    
    genero_mais_acustico = df_filtrado.groupby('track_genre')['acousticness'].mean().idxmax()
    valor_acustico = df_filtrado.groupby('track_genre')['acousticness'].mean().max()
    st.info(f"**Gênero mais acústico:** {genero_mais_acustico} ({valor_acustico:.2f})")