import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.carrega_dados import carregar_dados
import pandas as pd
import numpy as np

st.set_page_config(
    page_title='Tendências de Gênero',
    layout='wide'
)

st.title('Análise de Tendências por Gênero Musical')

df = carregar_dados()

if df.empty:
    st.stop()

# Tabs para diferentes visualizações
tab1, tab2, tab3 = st.tabs(["Rankings", "Comparações", "Análise Detalhada"])

with tab1:
    st.header("Rankings de Gêneros Musicais")
    
    # Filtros na sidebar
    with st.sidebar:
        st.header("Configurações de Ranking")
        top_n = st.slider("Top N Gêneros", 5, 20, 10)
        metrica_ranking = st.selectbox(
            "Métrica para Ranking",
            ["popularity", "danceability", "energy", "valence", "duration_min"]
        )
    
    # Gráfico 1: Barras Horizontais - Top Gêneros
    st.subheader(f"Top {top_n} Gêneros por {metrica_ranking.capitalize()}")
    
    df_top = (df.groupby('track_genre')[metrica_ranking]
              .mean()
              .sort_values(ascending=False)
              .head(top_n)
              .reset_index())
    
    fig_bar = px.bar(
        df_top,
        x=metrica_ranking,
        y='track_genre',
        orientation='h',
        color=metrica_ranking,
        color_continuous_scale='viridis',
        title=f'Média de {metrica_ranking.capitalize()} por Gênero',
        labels={
            metrica_ranking: metrica_ranking.capitalize(),
            'track_genre': 'Gênero Musical'
        }
    )
    
    fig_bar.update_layout(
        height=500,
        title_x=0.5,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()
    
    # Gráfico 2: Treemap - Quantidade de faixas por gênero
    st.subheader("🗺️ Distribuição de Faixas por Gênero")
    
    df_treemap = (df['track_genre']
                  .value_counts()
                  .head(20)
                  .reset_index()
                  .rename(columns={'track_genre': 'genero', 'count': 'quantidade'}))
    
    fig_treemap = px.treemap(
        df_treemap,
        path=['genero'],
        values='quantidade',
        title='Volume de Faixas por Gênero (Top 20)',
        color='quantidade',
        color_continuous_scale='Blues'
    )
    
    fig_treemap.update_layout(
        height=500,
        title_x=0.5
    )
    st.plotly_chart(fig_treemap, use_container_width=True)

with tab2:
    st.header("Comparação entre Gêneros")
    
    # Seletor de gêneros para comparar
    col_select1, col_select2 = st.columns(2)
    
    generos_disponiveis = sorted(df['track_genre'].unique())
    
    with col_select1:
        generos_comparar = st.multiselect(
            "Selecione até 5 gêneros para comparar",
            options=generos_disponiveis,
            default=df['track_genre'].value_counts().head(3).index.tolist(),
            max_selections=5
        )
    
    if not generos_comparar:
        st.warning("Selecione pelo menos um gênero para visualizar")
        st.stop()
    
    df_comp = df[df['track_genre'].isin(generos_comparar)]
    
    # Gráfico 3: Gráfico de Linhas - Comparação de múltiplas características
    st.subheader("📉 Comparação de Características Musicais")
    
    caracteristicas = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
    
    # Preparar dados para o gráfico de linhas
    df_comp_medio = df_comp.groupby('track_genre')[caracteristicas].mean().reset_index()
    
    # Transformar para formato longo
    df_long = df_comp_medio.melt(
        id_vars='track_genre',
        value_vars=caracteristicas,
        var_name='caracteristica',
        value_name='valor'
    )
    
    fig_line = px.line(
        df_long,
        x='caracteristica',
        y='valor',
        color='track_genre',
        markers=True,
        title='Perfil Musical Comparativo',
        labels={
            'caracteristica': 'Característica Musical',
            'valor': 'Valor Médio (0-1)',
            'track_genre': 'Gênero'
        }
    )
    
    fig_line.update_layout(
        height=500,
        title_x=0.5,
        hovermode='x unified'
    )
    fig_line.update_xaxes(tickangle=45)
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.divider()
    
    # Gráfico 4: Box Plot Comparativo - Popularidade
    st.subheader("Distribuição de Popularidade")
    
    fig_box_comp = px.box(
        df_comp,
        x='track_genre',
        y='popularity',
        color='track_genre',
        points='outliers',
        title='Comparação de Popularidade entre Gêneros',
        labels={
            'popularity': 'Popularidade (0-100)',
            'track_genre': 'Gênero'
        }
    )
    
    fig_box_comp.update_layout(
        height=500,
        title_x=0.5,
        showlegend=False
    )
    st.plotly_chart(fig_box_comp, use_container_width=True)
    
    # Tabela comparativa
    st.subheader("Tabela Comparativa")
    
    df_tabela = df_comp.groupby('track_genre').agg({
        'popularity': 'mean',
        'danceability': 'mean',
        'energy': 'mean',
        'valence': 'mean',
        'duration_min': 'mean',
        'track_name': 'count'
    }).round(2)
    
    df_tabela = df_tabela.rename(columns={'track_name': 'total_faixas'})
    df_tabela = df_tabela.sort_values('popularity', ascending=False)
    
    st.dataframe(df_tabela, use_container_width=True)

with tab3:
    st.header("Análise Detalhada por Gênero")
    
    # Seletor de gênero único
    genero_selecionado = st.selectbox(
        "Escolha um gênero para análise detalhada",
        options=sorted(df['track_genre'].unique())
    )
    
    df_genero = df[df['track_genre'] == genero_selecionado]
    
    # Métricas do gênero
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total de Faixas", len(df_genero))
    col2.metric("Popularidade Média", f"{df_genero['popularity'].mean():.1f}")
    col3.metric("Duração Média", f"{df_genero['duration_min'].mean():.2f} min")
    col4.metric("Artistas Únicos", df_genero['artists'].nunique())
    col5.metric("% Explícito", f"{(df_genero['explicit'].sum()/len(df_genero)*100):.1f}%")
    
    st.divider()
    
    # Gráfico 5: Histograma - Distribuição de Popularidade
    st.subheader(f"Distribuição de Popularidade - {genero_selecionado}")
    
    fig_hist = px.histogram(
        df_genero,
        x='popularity',
        nbins=30,
        title=f'Distribuição de Popularidade no gênero {genero_selecionado}',
        labels={'popularity': 'Popularidade', 'count': 'Quantidade de Faixas'},
        color_discrete_sequence=['#1DB954']
    )
    
    # Adicionar linha de média
    media_pop = df_genero['popularity'].mean()
    fig_hist.add_vline(
        x=media_pop,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média: {media_pop:.1f}",
        annotation_position="top"
    )
    
    fig_hist.update_layout(height=400, title_x=0.5)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.divider()
    
    # Gráfico 6: Scatter 3D - Análise Multidimensional
    st.subheader(f"Análise 3D - {genero_selecionado}")
    
    # Pegar amostra para performance
    df_sample = df_genero.sample(min(500, len(df_genero)))
    
    fig_3d = px.scatter_3d(
        df_sample,
        x='danceability',
        y='energy',
        z='valence',
        color='popularity',
        size='duration_min',
        hover_data=['track_name', 'artists'],
        title=f'Espaço Tridimensional de Características - {genero_selecionado}',
        labels={
            'danceability': 'Dançabilidade',
            'energy': 'Energia',
            'valence': 'Valência',
            'popularity': 'Popularidade'
        },
        color_continuous_scale='Turbo'
    )
    
    fig_3d.update_layout(
        height=600,
        title_x=0.5,
        scene=dict(
            xaxis_title='Dançabilidade',
            yaxis_title='Energia',
            zaxis_title='Valência'
        )
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.divider()
    
    # Top faixas do gênero
    st.subheader(f"Top 10 Faixas Mais Populares - {genero_selecionado}")
    
    df_top_tracks = (df_genero
                     .nlargest(10, 'popularity')[['track_name', 'artists', 'popularity', 'duration_min']]
                     .reset_index(drop=True))
    
    df_top_tracks.index += 1
    st.dataframe(df_top_tracks, use_container_width=True)
    
    # Características médias do gênero
    st.subheader("Perfil Musical Médio")
    
    col_perfil1, col_perfil2 = st.columns(2)
    
    with col_perfil1:
        caracteristicas_perfil = {
            'Dançabilidade': df_genero['danceability'].mean(),
            'Energia': df_genero['energy'].mean(),
            'Valência': df_genero['valence'].mean(),
            'Acusticidade': df_genero['acousticness'].mean(),
        }
        
        for nome, valor in caracteristicas_perfil.items():
            st.metric(nome, f"{valor:.3f}")
    
    with col_perfil2:
        caracteristicas_perfil2 = {
            'Instrumentalidade': df_genero['instrumentalness'].mean(),
            'Speechiness': df_genero['speechiness'].mean(),
            'Liveness': df_genero['liveness'].mean(),
            'Loudness': df_genero['loudness'].mean(),
        }
        
        for nome, valor in caracteristicas_perfil2.items():
            if nome == 'Loudness':
                st.metric(nome, f"{valor:.1f} dB")
            else:
                st.metric(nome, f"{valor:.3f}")

# Footer com informações
st.divider()
st.info("""
💡 **Dica de Navegação:** 
- Use a aba **Rankings** para identificar os gêneros mais populares
- A aba **Comparações** permite análise lado a lado de diferentes gêneros
- **Análise Detalhada** oferece um mergulho profundo em um gênero específico
""")