import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.carrega_dados import carregar_dados

# Configura as propriedades básicas da página (título da aba, layout)
st.set_page_config(
    page_title='Análise Musical',
    layout='wide'
)

# Título principal da aplicação
st.title('Análise de Características Musicais')

# Carrega o dataset para a memória
df = carregar_dados()

# Se o dataset estiver vazio, interrompe a execução para evitar erros
if df.empty:
    st.stop()

# Cria um container expansível para agrupar os filtros visualmente
with st.expander("Filtros de Dados", expanded=True):
    # Divide a largura em duas colunas: 75% (3 partes) e 25% (1 parte)
    col_genero, col_explicit = st.columns([3, 1])
    
    # Prepara a lista de gêneros ordenada para o dropdown
    todos_generos = sorted(df['track_genre'].unique())
    # Define os 10 gêneros mais comuns como seleção padrão
    top_10_padrao = df['track_genre'].value_counts().head(10).index.tolist()

    # Coluna da Esquerda: Filtro de Gêneros
    with col_genero:
        filtro_generos = st.multiselect(
            "Selecione os Gêneros",
            options=todos_generos,
            default=top_10_padrao,
            help="Filtre os dados por categoria musical"
        )

    # Coluna da Direita: Filtro de Conteúdo Explícito
    with col_explicit:
        filtro_explicit = st.selectbox(
            "Conteúdo Explícito",
            options=["Todos", "Sim", "Não"],
            index=0 # Padrão: Todos
        )

    # Slider único ocupando a largura total para filtrar Popularidade
    filtro_pop = st.slider(
        "Faixa de Popularidade",
        min_value=0,
        max_value=100,
        value=(0, 100) # Tupla indicando intervalo selecionado (início, fim)
    )

# Cria uma cópia para filtrar sem perder os dados originais
df_filtrado = df.copy()

# Aplica filtro de Gêneros
if filtro_generos:
    df_filtrado = df_filtrado[df_filtrado['track_genre'].isin(filtro_generos)]
else:
    # Validação: impede visualização sem gêneros selecionados
    st.warning("Selecione pelo menos um gênero para visualizar os dados")
    st.stop()

# Aplica filtro de Conteúdo Explícito
if filtro_explicit != "Todos":
    # Traduz a seleção "Sim/Não" para o valor real no banco de dados
    valor_para_filtrar = "Explicito" if filtro_explicit == "Sim" else "Nao Explicito"
    df_filtrado = df_filtrado[df_filtrado['explicit_str'] == valor_para_filtrar]

# Aplica filtro de Popularidade (range min e max)
df_filtrado = df_filtrado[
    (df_filtrado['popularity'] >= filtro_pop[0]) &
    (df_filtrado['popularity'] <= filtro_pop[1])
]

# Validação final pós-filtragem
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com essa combinação de filtros")
    st.stop()

# --- Seção de Métricas (KPIs) ---
col1, col2, col3, col4 = st.columns(4)
# Mostra contagem total e médias de atributos principais
col1.metric("Faixas Analisadas", len(df_filtrado))
col2.metric("Dançabilidade Média", f"{df_filtrado['danceability'].mean():.2f}")
col3.metric("Energia Média", f"{df_filtrado['energy'].mean():.2f}")
col4.metric("Valência Média", f"{df_filtrado['valence'].mean():.2f}")

st.divider()

# --- Gráfico 1: Scatter Plot (Dispersão) ---
st.subheader("Relação entre Dançabilidade e Energia")

# Cria gráfico de dispersão para ver correlação entre duas variáveis
fig_scatter = px.scatter(
    # Amostra de 1000 itens para não travar o navegador com excesso de pontos
    df_filtrado.sample(min(1000, len(df_filtrado))),
    x='danceability',
    y='energy',
    color='track_genre', # Cores diferentes por gênero
    size='popularity',   # Tamanho da bolinha indica popularidade
    hover_data=['track_name', 'artists', 'popularity'], # Dados extras no tooltip
    title='Dançabilidade vs Energia (tamanho = popularidade)',
    labels={
        'danceability': 'Dançabilidade (0-1)',
        'energy': 'Energia (0-1)',
        'track_genre': 'Gênero'
    },
    opacity=0.6 # Transparência para ver pontos sobrepostos
)

fig_scatter.update_layout(
    height=500,
    title_x=0.5,
    hovermode='closest'
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# --- Gráfico 2: Radar Chart (Gráfico de Aranha) ---
st.subheader("Perfil Musical Médio por Gênero")

# Define as colunas numéricas que formam o "DNA" musical
caracteristicas = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']

# Calcula a média de cada característica agrupada por gênero
df_radar = df_filtrado.groupby('track_genre')[caracteristicas].mean().reset_index()

# Inicializa uma figura vazia do Graph Objects
fig_radar = go.Figure()

# Loop para adicionar uma "camada" no radar para cada gênero
for idx, row in df_radar.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=[row[c] for c in caracteristicas], # Valores 
        theta=[c.capitalize() for c in caracteristicas],
        fill='toself', 
        name=row['track_genre'], 
        opacity=0.6
    ))

# Configura o layout polar
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

# --- Gráfico 3: Heatmap (Mapa de Calor) de Correlação ---
st.subheader("Mapa de Calor - Correlação entre Características")

col_corr1, col_corr2 = st.columns([2, 1])

with col_corr1:
    # Lista expandida de características de correlação
    caracteristicas_corr = ['danceability', 'energy', 'valence', 'acousticness', 
                            'instrumentalness', 'speechiness', 'liveness', 'popularity']
    
    # Pandas calcula a correlação de Pearson entre todas as colunas listadas
    corr_matrix = df_filtrado[caracteristicas_corr].corr()
    
    # Renderiza a matriz como imagem térmica
    fig_heatmap = px.imshow(
        corr_matrix,
        labels=dict(color="Correlação"),
        x=[c.capitalize() for c in caracteristicas_corr],
        y=[c.capitalize() for c in caracteristicas_corr],
        color_continuous_scale='RdBu_r', 
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
    
    **Vermelho intenso**: Correlação positiva forte (quando um sobe, o outro sobe).
    
    **Azul intenso**: Correlação negativa forte (quando um sobe, o outro desce).
    
    **Branco**: Sem correlação.
    
    Correlações próximas de ±1 indicam relação forte entre as características.
    """)

st.divider()

# --- Gráfico 4: Violin Plot (Distribuição + Densidade) ---
st.subheader("Distribuição de Valência Musical")

# Cria gráfico de violino para mostrar a densidade dos dados
fig_violin = px.violin(
    df_filtrado,
    x='track_genre',
    y='valence',
    color='track_genre',
    box=True,
    points='outliers', # Mostra pontos discrepantes
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

with st.expander("Sobre as Características Musicais"):
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

# --- Seção de Insights Automáticos ---
st.subheader("Insights da Análise")

col_insight1, col_insight2 = st.columns(2)

# Cálculos para encontrar os campeões em cada categoria
with col_insight1:
    # idxmax retorna o índice (nome do gênero) com o maior valor médio
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