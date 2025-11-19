import streamlit as st
import pandas as pd
from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title="Análise Spotify Tracks",
    page_icon="🎵",
    layout="wide"
)

df = carregar_dados()

st.title("Spotify Tracks: Análise Interativa")

if df.empty:
    st.warning("Aguardando o arquivo dataset.csv na pasta dataset.")
    st.stop()

st.markdown("---")

col_intro, col_metrics = st.columns([1.5, 1], gap="large")

with col_intro:
    st.markdown("### Sobre o Dashboard")
    st.markdown("""
    Bem-vindo(a)! Este projeto explora um dataset rico de faixas do Spotify para revelar os segredos por trás dos hits.
    
    **Nesta aplicação, você poderá:**
    * **Investigar** correlações entre energia, dancabilidade e positividade.
    * **Descobrir** quais gêneros dominam as paradas.
    * **Analisar** como a música explícita se comporta em relação à popularidade.
    
    Utilize o **menu lateral** para navegar entre as análises detalhadas.
    """)

with col_metrics:
    st.markdown("### Raio-X do Dataset")
    
    total_faixas = df.shape[0]
    total_artistas = df['artists'].nunique()
    total_generos = df['track_genre'].nunique()
    
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Faixas", f"{total_faixas:,}".replace(",", "."))
        st.metric("Artistas", total_artistas)
    with m2:
        st.metric("Gêneros", total_generos)
        st.metric("Atributos", df.shape[1])

st.markdown("---")

st.subheader(" O que você vai encontrar?")

row1 = st.columns(3)
with row1[0]:
    st.markdown("#### Visão Geral")
    st.caption("Panorama estatístico, filtros por categoria e distribuição de popularidade.")

with row1[1]:
    st.markdown("#### Análise Musical")
    st.caption("Gráficos de dispersão interativos para cruzar variáveis de áudio.")

with row1[2]:
    st.markdown("#### Tendências")
    st.caption("Comparativos de gêneros e seus perfis sonoros.")

st.markdown("---")

with st.expander("Clique para espiar a Amostra dos Dados (Top 10 linhas)"):
    st.dataframe(
        df.head(10),
        use_container_width=True,
        column_config={
            "track_name": "Música",
            "artists": "Artista",
            "album_name": "Álbum",
            "popularity": st.column_config.ProgressColumn(
                "Popularidade", format="%d", min_value=0, max_value=100
            ),
        }
    )
    st.caption(f"Mostrando as primeiras 10 linhas de {total_faixas} registros.")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** Use o modo 'Dark' do Streamlit para uma melhor experiência visual.")