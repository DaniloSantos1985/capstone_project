# ─── IMPORTAÇÕES ─────────────────────────────────────────────────────────────

import streamlit as st                        # Framework para criação da interface web
import pandas as pd                           # Manipulação de dados
import plotly.express as px                   # Criação de gráficos interativos
import numpy as np                            # Cálculos numéricos e geração de sequências
from utils.data_loader import load_data       # Função para carregar o CSV
from utils.charts import create_heatmap       # Função para criar o mapa de calor

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────

st.set_page_config(
    page_title="Análise",
    layout="wide"
)

st.title("Análise Avançada")
st.markdown("---")

# ─── LEITURA DAS CONFIGURAÇÕES DO SESSION STATE ──────────────────────────────

# Lê as configurações salvas na página de Ferramentas
# .get(chave, valor_padrão) → usa o valor padrão se a configuração não foi salva ainda
chart_theme    = st.session_state.get('chart_theme', 'plotly')    # Tema visual dos gráficos
show_grid      = st.session_state.get('show_grid', True)          # Exibir linhas de grid
decimal_places = st.session_state.get('decimal_places', 2)        # Casas decimais
date_format    = st.session_state.get('date_format', '%d-%m-%Y')  # Formato de data
rows_per_page  = st.session_state.get('rows_per_page', 10)        # Linhas por página

# ─── FUNÇÃO: FORMATAÇÃO BRASILEIRA DO EIXO Y ─────────────────────────────────

def formato_brasileiro(y_min, y_max, decimal_places, n_ticks=5):
    """
    Gera tickvals e ticktext no formato brasileiro R$ 000.000,00
    
    Parâmetros:
    y_min         → valor mínimo do eixo Y
    y_max         → valor máximo do eixo Y
    decimal_places → número de casas decimais
    n_ticks       → número de marcações no eixo Y (padrão: 5)
    
    Retorna:
    tickvals → array com os valores numéricos das marcações
    ticktext → lista com os rótulos formatados em R$ 000.000,00
    """
    # np.linspace → gera n_ticks valores igualmente espaçados entre y_min e y_max
    tickvals = np.linspace(y_min, y_max, n_ticks)

    # Converte cada valor para o formato brasileiro
    # Passo 1: f"R$ {v:,.2f}" → "R$ 680,000.00" (padrão americano com prefixo)
    # Passo 2: .replace(",", "X") → "R$ 680X000.00" (substitui vírgula por X temporário)
    # Passo 3: .replace(".", ",") → "R$ 680X000,00" (substitui ponto por vírgula)
    # Passo 4: .replace("X", ".") → "R$ 680.000,00" (substitui X por ponto — formato BR)
    ticktext = [
        f"R$ {v:,.{decimal_places}f}"
        .replace(",", "X").replace(".", ",").replace("X", ".")
        for v in tickvals
    ]
    return tickvals, ticktext

# ─── CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────

# Carrega o CSV usando cache — evita recarregar a cada interação do usuário
df = load_data()

if df is not None:

    # Cria 3 abas navegáveis na página
    tab1, tab2, tab3 = st.tabs(["Tendências", "Análise Temporal", "Insights dos Clientes"])

    # =========================================================================
    # ABA 1 — TENDÊNCIAS
    # =========================================================================
    with tab1:
        st.subheader("Tendência de Receita ao Longo do Tempo")

        # Selectbox para o usuário escolher o nível de agrupamento temporal
        agg_level = st.selectbox(
            'Nível de Agregação',
            options=['Diário', 'Semanal', 'Mensal', 'Trimestral']
        )

        # Cria uma cópia do DataFrame para não modificar os dados originais
        df_trend = df.copy()

        # Agrupa os dados conforme o nível de agregação selecionado
        if agg_level == 'Diário':
            # Agrupa por dia — soma a receita de cada data
            df_trend = df_trend.groupby('Data')['Receita'].sum().reset_index()
        elif agg_level == 'Semanal':
            # resample('W-Mon') → agrupa por semana começando na Segunda-feira
            df_trend = df_trend.resample('W-Mon', on='Data')['Receita'].sum().reset_index()
        elif agg_level == 'Mensal':
            # resample('ME') → agrupa por mês (ME = Month End — fim do mês)
            df_trend = df_trend.resample('ME', on='Data')['Receita'].sum().reset_index()
        else:
            # resample('QE') → agrupa por trimestre (QE = Quarter End — fim do trimestre)
            df_trend = df_trend.resample('QE', on='Data')['Receita'].sum().reset_index()

        # Define o eixo Y começando em 0
        # Margem de 10% no topo para não cortar o ponto mais alto do gráfico
        y_min_trend = 0
        y_max_trend = df_trend['Receita'].max() * 1.1 if not df_trend.empty else 100

        # Gera os valores e rótulos do eixo Y no formato brasileiro
        tickvals, ticktext = formato_brasileiro(
            y_min_trend,
            y_max_trend,
            decimal_places,
            n_ticks=5
        )

        # Cria o gráfico de linha com Plotly Express
        # markers=True → exibe pontos em cada data do gráfico
        fig = px.line(
            df_trend,
            x='Data',
            y='Receita',
            title=f'Tendência de Receita ({agg_level})',
            markers=True,
            template=chart_theme  # Tema salvo nas configurações
        )

        fig.update_layout(
            height=500,
            xaxis_showgrid=show_grid,   # Grid no eixo X conforme configuração
            yaxis_showgrid=show_grid,   # Grid no eixo Y conforme configuração
            yaxis=dict(
                range=[y_min_trend, y_max_trend],  # Limites do eixo Y
                tickvals=tickvals,                  # Valores numéricos das marcações
                ticktext=ticktext,                  # Rótulos em formato brasileiro
                tickangle=0                         # Rótulos na horizontal
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================================================================
    # ABA 2 — ANÁLISE TEMPORAL
    # =========================================================================
    with tab2:
        st.subheader("Análise baseada no tempo")

        # Exibe o mapa de calor de vendas por Dia da Semana vs Mês
        st.plotly_chart(create_heatmap(df), use_container_width=True)

        # ─── VENDAS POR DIA DA SEMANA ─────────────────────────────────────────

        st.markdown("### Vendas por Dia da Semana")

        df_dow = df.copy()

        # Dicionário de tradução dos dias da semana — inglês para português
        translate_days = {
            'Monday':    'Segunda-feira',
            'Tuesday':   'Terça-feira',
            'Wednesday': 'Quarta-feira',
            'Thursday':  'Quinta-feira',
            'Friday':    'Sexta-feira',
            'Saturday':  'Sábado',
            'Sunday':    'Domingo'
        }

        # Extrai o nome do dia da semana e traduz para português
        df_dow['Dia da Semana'] = df_dow['Data'].dt.day_name().map(translate_days)

        # Agrupa por dia da semana, soma a receita e reordena de Segunda a Domingo
        # reindex → garante a ordem correta dos dias mesmo se algum estiver faltando
        dow_sales = df_dow.groupby('Dia da Semana')['Receita'].sum().reindex([
            'Segunda-feira', 'Terça-feira', 'Quarta-feira',
            'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
        ]).reset_index()

        # Eixo Y começando em 0 com margem de 10% no topo
        y_min_dow = 0
        y_max_dow = dow_sales['Receita'].max() * 1.1 if not dow_sales.empty else 100

        # Gera os valores e rótulos do eixo Y no formato brasileiro
        tickvals_dow, ticktext_dow = formato_brasileiro(
            y_min_dow,
            y_max_dow,
            decimal_places,
            n_ticks=5
        )

        # Cria o gráfico de barras por dia da semana
        # color='Dia da Semana' → cada dia recebe uma cor diferente automaticamente
        fig_dow = px.bar(
            dow_sales,
            x='Dia da Semana',
            y='Receita',
            title='Receita por Dia da Semana',
            labels={'Receita': 'Total de Receita', 'Dia da Semana': ''},
            color='Dia da Semana',
            template=chart_theme
        )

        fig_dow.update_layout(
            xaxis_showgrid=show_grid,
            yaxis_showgrid=show_grid,
            yaxis=dict(
                range=[y_min_dow, y_max_dow],
                tickvals=tickvals_dow,
                ticktext=ticktext_dow,
                tickangle=0
            )
        )

        st.plotly_chart(fig_dow, use_container_width=True)

        # ─── COMPARAÇÃO MENSAL DE RECEITA ─────────────────────────────────────

        st.markdown("### Comparação Mensal de Receita")

        df_monthly = df.copy()

        # Dicionário de tradução dos meses — inglês para português
        translate_months = {
            'January':   'Janeiro',   'February':  'Fevereiro',
            'March':     'Março',     'April':     'Abril',
            'May':       'Maio',      'June':      'Junho',
            'July':      'Julho',     'August':    'Agosto',
            'September': 'Setembro',  'October':   'Outubro',
            'November':  'Novembro',  'December':  'Dezembro'
        }

        df_monthly['Mês'] = df_monthly['Data'].dt.month_name().map(translate_months)

        # .astype(str) → converte o ano para string
        # Necessário para o Plotly tratar o ano como categoria e não como número contínuo
        df_monthly['Ano'] = df_monthly['Data'].dt.year.astype(str)

        # Define a ordem cronológica dos meses
        ordem_meses = [
            'Janeiro', 'Fevereiro', 'Março',    'Abril',   'Maio',     'Junho',
            'Julho',   'Agosto',    'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]

        # pd.Categorical → informa ao pandas que 'Mês' é uma categoria ordenada
        df_monthly['Mês'] = pd.Categorical(df_monthly['Mês'], categories=ordem_meses, ordered=True)

        # Agrupa por Ano e Mês somando a receita de cada combinação
        monthly_sales = df_monthly.groupby(['Ano', 'Mês'])['Receita'].sum().reset_index()

        # Ordena pelo mês antes de plotar para garantir ordem cronológica
        monthly_sales = monthly_sales.sort_values('Mês')

        # Eixo Y começando em 0 com margem de 10% no topo
        y_min_monthly = 0
        y_max_monthly = monthly_sales['Receita'].max() * 1.1 if not monthly_sales.empty else 100

        # Gera os valores e rótulos do eixo Y no formato brasileiro
        tickvals_monthly, ticktext_monthly = formato_brasileiro(
            y_min_monthly,
            y_max_monthly,
            decimal_places,
            n_ticks=5
        )

        # Cria o gráfico de barras agrupadas por mês e ano
        # barmode='group' → barras lado a lado (não empilhadas)
        # category_orders → garante a ordem correta dos meses no eixo X
        fig_monthly = px.bar(
            monthly_sales,
            x='Mês',
            y='Receita',
            color='Ano',
            barmode='group',
            title='Comparação Mensal de Receita por Ano',
            labels={'Receita': 'Total de Receita', 'Mês': '', 'Ano': 'Ano'},
            category_orders={'Mês': ordem_meses},
            template=chart_theme
        )

        fig_monthly.update_layout(
            xaxis_showgrid=show_grid,
            yaxis_showgrid=show_grid,
            yaxis=dict(
                range=[y_min_monthly, y_max_monthly],
                tickvals=tickvals_monthly,
                ticktext=ticktext_monthly,
                tickangle=0
            )
        )

        st.plotly_chart(fig_monthly, use_container_width=True)

    # =========================================================================
    # ABA 3 — INSIGHTS DOS CLIENTES
    # =========================================================================
    with tab3:
        st.subheader('Insights dos clientes')

        # Divide a área em 2 colunas — col1 menor (pizza) | col2 maior (linha)
        col1, col2 = st.columns([1, 3])

        with col1:
            # Agrupa por tipo de cliente e soma a receita de cada tipo
            customer_dist = df.groupby('Tipo_cliente')['Receita'].sum().reset_index()

            # Gráfico de pizza/donut — hole=0.4 cria o furo central
            fig_cust = px.pie(
                customer_dist,
                values='Receita',
                names='Tipo_cliente',
                title='Receita por Tipo Cliente',
                hole=0.4,
                template=chart_theme
            )

            st.plotly_chart(fig_cust, use_container_width=True)

        with col2:
            df_cust_trend = df.copy()

            # Converte a data para período mensal e extrai o início do mês
            # to_period('M') → agrupa por mês | dt.start_time → pega o dia 1 do mês
            df_cust_trend['Mês'] = df_cust_trend['Data'].dt.to_period('M').dt.start_time

            # Agrupa por Mês e Tipo de Cliente somando a receita de cada combinação
            cust_trend = df_cust_trend.groupby(['Mês', 'Tipo_cliente'])['Receita'].sum().reset_index()

            # Eixo Y começando em 0 com margem de 10% no topo
            y_min_cust = 0
            y_max_cust = cust_trend['Receita'].max() * 1.1 if not cust_trend.empty else 100

            # Gera os valores e rótulos do eixo Y no formato brasileiro
            tickvals_trend, ticktext_trend = formato_brasileiro(
                y_min_cust,
                y_max_cust,
                decimal_places,
                n_ticks=5
            )

            # Gráfico de linha — cada tipo de cliente recebe uma cor diferente
            fig_trend = px.line(
                cust_trend,
                x='Mês',
                y='Receita',
                color='Tipo_cliente',
                title='Tendência de Receita por Tipo de Cliente',
                template=chart_theme
            )

            fig_trend.update_layout(
                xaxis_showgrid=show_grid,
                yaxis_showgrid=show_grid,
                yaxis=dict(
                    range=[y_min_cust, y_max_cust],
                    tickvals=tickvals_trend,
                    ticktext=ticktext_trend,
                    tickangle=0
                )
            )

            st.plotly_chart(fig_trend, use_container_width=True)

        # ─── ANÁLISE DE TRANSAÇÃO ─────────────────────────────────────────────

        st.markdown('### Análise de Transação')

        # Agrupa por tipo de cliente e calcula métricas agregadas
        # Receita    → média de receita por transação
        # Quantidade → média de quantidade por transação
        # Vendas     → contagem total de transações (count)
        # .round(decimal_places) → arredonda conforme configuração do usuário
        avg_transaction = df.groupby('Tipo_cliente').agg({
            'Receita':    'mean',
            'Quantidade': 'mean',
            'Vendas':     'count'
        }).round(decimal_places).reset_index()

        # Renomeia as colunas para nomes mais amigáveis em português
        avg_transaction.columns = [
            'Tipo de Cliente',
            'Média da Receita',
            'Média da Quantidade',
            'Número de Transações'
        ]

        # Exibe a tabela com formatação brasileira na coluna de receita
        # style.format → aplica formatação personalizada por coluna
        # lambda x → converte cada valor para o formato R$ 000.000,00
        st.dataframe(
            avg_transaction.style.format({
                "Média da Receita": lambda x: f"R$ {x:,.{decimal_places}f}"
                    .replace(",", "X").replace(".", ",").replace("X", "."),
                "Média da Quantidade": f"{{:.{decimal_places}f}}"  # Casas decimais dinâmicas
            }),
            use_container_width=True
        )

else:
    # Exibe mensagem de erro caso os dados não sejam carregados corretamente
    st.error('Não foi possível carregar os dados. Verifique o seu arquivo de dados.')