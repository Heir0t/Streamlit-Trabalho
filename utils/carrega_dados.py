import pandas as pd
import streamlit as st
import os

@st.cache_data
def carregar_dados():
    caminho_arquivo = './dataset/dataset.csv'
  
    df_original = pd.read_csv(caminho_arquivo)
    
    df = df_original.copy()

    df = df.drop_duplicates(subset=['track_id'])

    df = df.dropna()

    df['duration_min'] = df['duration_ms'] / 60000

    df['explicit_str'] = df['explicit'].map({True: 'Explicito', False: 'Nao Explicito'})

    def categorizar_popularidade(val):
        if val < 20: return 'Baixa'
        elif val < 50: return 'Media'
        elif val < 80: return 'Alta'
        else: return 'Hit Global'
    
    df['classe_popularidade'] = df['popularity'].apply(categorizar_popularidade)

    df['classe_popularidade'] = pd.Categorical(
        df['classe_popularidade'], 
        categories=['Baixa', 'Media', 'Alta', 'Hit Global'], 
        ordered=True
    )

    return df