# Dashboard de Análise de Características Musicais

Este projeto é uma aplicação web interativa desenvolvida em Python com Streamlit para análise de um dataset musical. O objetivo é identificar padrões entre gêneros musicais, correlações entre atributos de áudio (como dançabilidade e energia) e tendências de popularidade.

## Objetivo do Dashboard

O dashboard foi desenvolvido para facilitar a visualização e interpretação de características musicais presentes no dataset. Ele auxilia na identificação de padrões entre gêneros, análise de popularidade, comparação de atributos sonoros e compreensão do "DNA musical" de cada categoria.

## Como Navegar Entre as Seções

O dashboard está dividido em abas e seções interativas. A navegação funciona da seguinte forma:

* **Aba principal**: Oferece visão geral dos filtros e visualizações.
* **Cada gráfico**: Pode ser acessado rolando a página ou navegando pelo menu lateral (se configurado no Streamlit).
* **Filtros**: Localizados no topo/lateral da interface, atualizam todas as visualizações em tempo real.

## Como os Filtros Influenciam os Dados

Os filtros aplicados—como gênero, conteúdo explícito e faixa de popularidade—afetam diretamente todas as visualizações exibidas no dashboard. Assim que qualquer filtro é ajustado:

* Os gráficos são recalculados com base apenas nos dados filtrados.
* Correlações, distribuições e insights passam a refletir somente o subconjunto selecionado.
* Isso permite comparar cenários específicos, como "somente gêneros eletrônicos" ou "músicas populares sem conteúdo explícito".

## Funcionalidades

O dashboard oferece as seguintes visualizações e interações:

* **Filtros Dinâmicos**: Filtragem por Gênero, Conteúdo Explícito e Faixa de Popularidade.
* **Scatter Plot Interativo**: Relação entre Dançabilidade vs. Energia, dimensionado pela popularidade.
* **Radar Chart**: Perfil médio das características de áudio (DNA musical) por gênero.
* **Mapa de Calor (Heatmap)**: Matriz de correlação entre variáveis numéricas.
* **Violin Plot**: Distribuição de valência (positividade) por gênero.
* **Insights Automáticos**: Identificação automática dos gêneros "campeões" em categorias como dançabilidade e energia.

## Tecnologias Utilizadas

* **Python**
* **Streamlit**: Para criação da interface web.
* **Plotly Express & Graph Objects**: Para visualizações interativas.
* **Pandas**: Para manipulação e filtragem de dados.

## Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/Heir0t/Streamlit-Trabalho
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
streamlit 01_Principal.py
```

O navegador abrirá automaticamente no endereço **[http://localhost:8501](http://localhost:8501)**.

## Sobre os Dados

Os dados utilizados neste projeto contêm métricas de áudio padronizadas. As características incluem:

* **Danceability**: O quão adequada a faixa é para dançar.
* **Energy**: Medida de intensidade e atividade.
* **Valence**: A "positividade" musical da faixa.
* **Acousticness, Instrumentalness, Speechiness**, entre outros.
