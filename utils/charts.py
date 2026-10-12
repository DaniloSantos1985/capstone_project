# Importação das bibliotecas necessárias
import plotly.express as px          # Gráficos de alto nível — linha, pizza, barras
import plotly.graph_objects as go    # Gráficos de baixo nível — heatmap personalizado
import pandas as pd                  # Manipulação de dados
import streamlit as st

# ─── FUNÇÃO: TENDÊNCIA DE RECEITA ────────────────────────────────────────────

def create_revenue_trend(df):
    """
    Cria um gráfico de linha mostrando a tendência de receita ao longo do tempo.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados de vendas.
    
    Retorna:
    plotly.graph_objects.Figure: Gráfico de linha da tendência de receita.
    """

    # Agrupa os dados por data e soma a receita diária
    # reset_index() transforma o índice 'Data' de volta em coluna
    daily_revenue = df.groupby('Data')['Receita'].sum().reset_index()

    # Cria o gráfico de linha com Plotly Express
    # x='Data' → eixo horizontal | y='Receita' → eixo vertical
    # labels → renomeia os eixos para exibição no gráfico
    fig = px.line(
        daily_revenue, 
        x='Data', 
        y='Receita', 
        title='Tendência de Receita ao Longo do Tempo',        
        labels={'Receita': 'Receita (R$)', 'Data': 'Data'},
        template=st.session_state.get('chart_theme') # ✅ aplica o tema
    )
    
    fig.update_layout(
        hovermode='x unified',   # Exibe tooltip unificado ao passar o mouse na vertical
        plot_bgcolor='white',    # Define fundo do gráfico como branco
        height=400,              # Altura do gráfico em pixels
        showlegend=st.session_state.get('show_grid', True),  # ✅ aplica o grid
    )

    return fig


# ─── FUNÇÃO: DISTRIBUIÇÃO DE RECEITA POR REGIÃO ──────────────────────────────

def create_region_pie(df):
    """
    Cria um gráfico de pizza mostrando a distribuição de receita por região.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados de vendas.
    
    Retorna:
    plotly.graph_objects.Figure: Gráfico de pizza da distribuição de receita por região.
    """

    # Agrupa os dados por região e soma a receita de cada uma
    region_revenue = df.groupby('Região')['Receita'].sum().reset_index()

    # Cria o gráfico de pizza (donut) com Plotly Express
    # names='Região'  → categorias das fatias
    # values='Receita' → tamanho de cada fatia
    # hole=0.4         → cria o furo central transformando em gráfico donut (40% do raio)
    fig = px.pie(
        region_revenue, 
        names='Região', 
        values='Receita', 
        title='Distribuição de Receita por Região',
        hole=0.4,
        template=st.session_state.get('chart_theme') # ✅ aplica o tema
    )
    
    # Exibe o percentual e o nome da região dentro de cada fatia
    fig.update_traces(textposition='inside', textinfo='percent+label')   

    return fig


# ─── FUNÇÃO: RECEITA POR PRODUTO ─────────────────────────────────────────────

def create_product_bar(df):
    """
    Cria um gráfico de barras mostrando a receita por produto.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados de vendas.
    
    Retorna:
    plotly.graph_objects.Figure: Gráfico de barras da receita por produto.
    """

    # Agrupa por produto, soma as vendas e ordena do maior para o menor
    # ascending=False → ordem decrescente (maior vendas primeiro)
    product_sales = df.groupby('Produto')['Vendas'].sum().sort_values(ascending=False).reset_index()

    # Cria o gráfico de barras horizontal com Plotly Express
    # x='Vendas'  → comprimento das barras (eixo horizontal)
    # y='Produto' → categorias (eixo vertical)
    # color='Produto' → cada produto recebe uma cor diferente automaticamente
    fig = px.bar(
        product_sales, 
        x='Vendas', 
        y='Produto', 
        title='Vendas por Produto',
        labels={'Vendas': 'Total de Vendas', 'Produto': 'Produto'},
        color='Produto',
        template=st.session_state.get('chart_theme') # ✅ aplica o tema
    )
    
    fig.update_layout(
        height=400,             # Altura do gráfico em pixels
        plot_bgcolor='white',   # Define fundo do gráfico como branco
    )

    return fig


# ─── FUNÇÃO: MAPA DE CALOR ───────────────────────────────────────────────────

def create_heatmap(df):
    """
    Cria um mapa de calor mostrando vendas por dia da semana e mês.
        
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados de vendas.
        
    Retorna:
    plotly.graph_objects.Figure: Mapa de calor de vendas.
    """

    # Cria uma cópia para não modificar o DataFrame original
    df_copy = df.copy()

    # Dicionário de tradução dos dias da semana — inglês para português
    # day_name() retorna em inglês por padrão, então precisamos traduzir
    translate_days = {
        'Monday':    'Segunda-feira',
        'Tuesday':   'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday':  'Quinta-feira',
        'Friday':    'Sexta-feira',
        'Saturday':  'Sábado',
        'Sunday':    'Domingo'
    }

    # Dicionário de tradução dos meses — inglês para português
    # month_name() retorna em inglês por padrão, então precisamos traduzir
    translate_months = {
        'January':   'Janeiro',   'February':  'Fevereiro',
        'March':     'Março',     'April':     'Abril',
        'May':       'Maio',      'June':      'Junho',
        'July':      'Julho',     'August':    'Agosto',
        'September': 'Setembro',  'October':   'Outubro',
        'November':  'Novembro',  'December':  'Dezembro'
    }

    # Extrai o nome do dia da semana e traduz para português usando o dicionário
    df_copy['Dia da Semana'] = df_copy['Data'].dt.day_name().map(translate_days)

    # Extrai o nome do mês e traduz para português usando o dicionário
    df_copy['Mês'] = df_copy['Data'].dt.month_name().map(translate_months)

    # Agrupa por dia da semana e mês, somando as vendas de cada combinação
    heatmap_data = df_copy.groupby(['Dia da Semana', 'Mês'])['Vendas'].sum().reset_index()

    # Transforma o DataFrame em tabela pivô
    # index='Dia da Semana' → linhas do heatmap
    # columns='Mês'         → colunas do heatmap
    # values='Vendas'       → valores que preenchem as células
    heatmap_pivot = heatmap_data.pivot(index='Dia da Semana', columns='Mês', values='Vendas')

    # Reordena as linhas na ordem correta dos dias da semana
    # Sem isso os dias ficam em ordem alfabética
    days_order = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    heatmap_pivot = heatmap_pivot.reindex(days_order)

    # Reordena as colunas na ordem cronológica dos meses
    # Sem isso os meses ficam em ordem alfabética
    months_order = [
        'Janeiro', 'Fevereiro', 'Março',    'Abril',   'Maio',     'Junho',
        'Julho',   'Agosto',    'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    heatmap_pivot = heatmap_pivot.reindex(columns=months_order)

    # Cria o heatmap com Plotly Graph Objects
    # z → matriz de valores (intensidade das cores)
    # x → colunas do heatmap (meses)
    # y → linhas do heatmap (dias da semana)
    # colorscale='Blues' → escala de cores em tons de azul
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='Blues'        
    ))
    
    fig.update_layout(
        title='Mapa de calor de vendas: Dia da Semana vs Mês',
        height=400
    )
    
    return fig