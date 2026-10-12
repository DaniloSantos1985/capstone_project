# ─── CONFIGURAÇÃO DO PATH ────────────────────────────────────────────────────

import sys
import os

# Adiciona a raiz do projeto ao PATH do Python
# Necessário para que o Python encontre a pasta utils/ ao rodar páginas da pasta pages/
# os.path.abspath(__file__)        → caminho absoluto deste arquivo
# os.path.dirname(...)             → pasta pages/
# os.path.dirname(dirname(...))    → pasta raiz do projeto (sobe dois níveis)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import streamlit as st    # Framework para criação da interface web
import pandas as pd       # Manipulação de dados

# Funções customizadas de carregamento, filtragem e cálculo de métricas
from utils.data_loader import load_data, filter_data, calculate_metrics

# Funções customizadas para criação dos gráficos
from utils.charts import create_revenue_trend, create_region_pie, create_product_bar

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────

# Define título da aba do navegador e layout em tela cheia
st.set_page_config(
    page_title="Dashboard",
    layout="wide",
)

# Título principal e linha divisória
st.title("Dashboard de Vendas")
st.markdown('---')

# ─── CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────

# Carrega o CSV usando cache — evita recarregar a cada interação do usuário
df = load_data()

if df is not None:

    # ─── SIDEBAR: FILTROS ────────────────────────────────────────────────────

    st.sidebar.header("Filtros")
    
    # Filtro de intervalo de datas
    # value → define as datas inicial e final padrão (min e max do dataset)
    # min_value/max_value → limita a seleção ao intervalo disponível nos dados
    date_range = st.sidebar.date_input(
        "Selecione o intervalo de datas:",
        value=[df['Data'].min(), df['Data'].max()],
        min_value=df['Data'].min(),
        max_value=df['Data'].max()
    )

    # Filtro de regiões
    # unique().tolist() → obtém todas as regiões únicas do dataset
    # default=all_regions → todas as regiões selecionadas por padrão
    all_regions = df['Região'].unique().tolist()
    selected_regions = st.sidebar.multiselect(
        "Selecione as regiões:",
        options=all_regions,
        default=all_regions
    )

    # Filtro de produtos
    # unique().tolist() → obtém todos os produtos únicos do dataset
    # default=all_products → todos os produtos selecionados por padrão
    all_products = df['Produto'].unique().tolist()
    selected_products = st.sidebar.multiselect(
        "Selecione os produtos:",
        options=all_products,
        default=all_products
    )

    # ─── PROCESSAMENTO DOS DADOS FILTRADOS ───────────────────────────────────

    # Aplica os três filtros (data, região e produto) ao DataFrame original
    filtered_df = filter_data(df, date_range, selected_regions, selected_products)

    # Calcula as métricas agregadas com base nos dados filtrados
    metrics = calculate_metrics(filtered_df)

    # ─── CARDS DE MÉTRICAS ───────────────────────────────────────────────────

    # Divide a área em 5 colunas de tamanho igual
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # Total de Receita com delta mostrando % em relação ao total geral
        # :,.2f → formato com separador de milhar e 2 casas decimais
        st.metric(
            "Total de Receita", 
            f"R$ {metrics['Total de Receita']:,.2f}".replace(',','x').replace('.',',').replace('x','.'),
            delta=f"{(metrics['Total de Receita']/df['Receita'].sum()*100):.1f}% do total"         
        )

    with col2:
        # Total de Vendas com delta mostrando número de transações
        # :,.0f → formato com separador de milhar sem casas decimais
        st.metric(
            "Total de Vendas", 
            f"R$ {metrics['Total de Vendas']:,.2f}".replace(',','x').replace('.',',').replace('x','.'),
            delta=f"{metrics['Número de Transações']:,} transações"
        )

    with col3:
        # Receita média por transação no período filtrado
        st.metric(
            "Média de Receita",
            f"R$ {metrics['Média de Receita']:,.2f}".replace(',','x').replace('.',',').replace('x','.')            
        )

    with col4:
        # Total de unidades vendidas no período filtrado
        # :, → formato com separador de milhar
        st.metric(
            "Quantidade Total", 
            f"{metrics['Quantidade Total']:,}".replace(',','.')            
        )

    with col5:
        # Número total de registros no DataFrame filtrado
        st.metric(
            "Transações", 
            f"{len(filtered_df):,}".replace(',','.'),
        )

    st.markdown('---')

    # ─── VISUALIZAÇÕES ───────────────────────────────────────────────────────

    st.subheader("Tendência de Receita ao Longo do Tempo")

    # Gráfico de linha — tendência de receita diária ao longo do tempo
    # use_container_width=True → ocupa toda a largura disponível
    st.plotly_chart(create_revenue_trend(filtered_df), use_container_width=True)

    # Divide a área em 2 colunas para exibir dois gráficos lado a lado
    col1, col2 = st.columns(2)  

    with col1:
        # Gráfico de pizza/donut — distribuição de receita por região
        st.plotly_chart(create_region_pie(filtered_df), use_container_width=True)

    with col2:
        # Gráfico de barras — vendas totais por produto
        st.plotly_chart(create_product_bar(filtered_df), use_container_width=True)

    # ─── TABELA DE DADOS FILTRADOS ───────────────────────────────────────────

    st.markdown('---')
    st.subheader("Tabela de Dados Filtrados")

    # Divide em 2 colunas — col1 vazia (espaçador) e col2 com o selectbox
    # proporção [3, 1] → col2 ocupa 25% da largura
    col1, col2 = st.columns([3, 1])

    with col2:
        # Selectbox para escolher quantos registros exibir na tabela
        show_records = st.selectbox("Mostrar tabela de dados", [10, 25, 50, 100, 'All'])

    # Exibe todos os registros ou apenas os N primeiros conforme seleção
    if show_records == 'All':
        #st.dataframe(filtered_df, use_container_width=True, height=400)
        st.dataframe(
            filtered_df.style.format({
                "Receita": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            }),
            use_container_width=True,
            height=400
        )
        
    else:
        # .head(show_records) → limita a exibição ao número selecionado
        st.dataframe(
            filtered_df.head(show_records).style.format({
                "Receita": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            }),
            use_container_width=True,
            height=400
        )
        #st.dataframe(filtered_df.head(show_records), use_container_width=True, height=400)

    # ─── DOWNLOAD DOS DADOS ──────────────────────────────────────────────────

    # Converte o DataFrame filtrado para CSV em memória
    # index=False → não inclui a coluna de índice numérico
    # .encode('utf-8') → codifica para bytes, necessário para o download
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    # Botão de download — gera o arquivo CSV para o usuário baixar
    # label → texto exibido no botão
    # data  → conteúdo do arquivo
    # file_name → nome do arquivo ao salvar
    # mime → tipo do arquivo (text/csv)
    # type="primary" → estilo do botão em destaque (azul)
    st.download_button(
        label="Baixar dados filtrados como CSV",
        data=csv,
        file_name="dados_filtrados_vendas.csv",
        mime="text/csv",
        type="primary",
    )

else:
    # Exibe mensagem de erro caso os dados não sejam carregados corretamente
    st.error("Falha ao carregar os dados. Verifique o arquivo CSV e tente novamente.")