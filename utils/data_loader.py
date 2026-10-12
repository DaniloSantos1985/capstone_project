# Importação das bibliotecas necessárias
import pandas as pd      # Manipulação e leitura de dados
import streamlit as st   # Interface web e exibição de erros
import os                # Manipulação de caminhos de arquivos no sistema operacional

# ─── FUNÇÃO: CARREGAR DADOS ──────────────────────────────────────────────────

# @st.cache_data — armazena o resultado em cache após a primeira execução
# Evita recarregar o CSV toda vez que o usuário interage com a página
# O cache é mantido até que o arquivo mude ou o app seja reiniciado
@st.cache_data
def load_data(file_path=None):
    """
    Carrega os dados de um arquivo CSV e retorna um DataFrame do pandas.
        
    Parâmetros:
    file_path (str): Caminho para o arquivo CSV a ser carregado.
        
    Retorna:
    pd.DataFrame: DataFrame contendo os dados carregados.
    """

    # Se nenhum caminho for fornecido, define o caminho automaticamente
    if file_path is None:
        # os.path.abspath(__file__) → caminho absoluto do arquivo data_loader.py
        # os.path.dirname(...)      → pasta onde o data_loader.py está (utils/)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Sobe um nível (../) saindo de utils/ e entra na pasta data/
        # Resultado: .../capstone_project/data/sample_data.csv
        file_path = os.path.join(base_dir, '..', 'data', 'sample_data.csv')

    try:
        # Lê o arquivo CSV e converte em DataFrame do pandas
        df = pd.read_csv(file_path)

        # Converte a coluna 'Data' para o formato datetime
        # Necessário para operações de filtro e agrupamento por data
        df['Data'] = pd.to_datetime(df['Data'])
        return df

    except Exception as e:
        # Exibe mensagem de erro no Streamlit caso o arquivo não seja encontrado
        # Retorna None para que o código principal trate a ausência dos dados
        st.error(f"Erro ao carregar os dados: {e}")
        return None


# ─── FUNÇÃO: FILTRAR DADOS ───────────────────────────────────────────────────

def filter_data(df, data_range, regions, products):
    """
    Filtra os dados com base no intervalo de datas, regiões e produtos fornecidos.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados a serem filtrados.
    data_range (tuple): Tupla contendo a data inicial e final para o filtro.
    regions (list): Lista de regiões para filtrar.
    products (list): Lista de produtos para filtrar.
    
    Retorna:
    pd.DataFrame: DataFrame filtrado com base nos critérios fornecidos.
    """

    # Cria uma cópia para não modificar o DataFrame original
    filtered_df = df.copy()

    # Converte as datas do filtro para datetime
    # Necessário pois o st.date_input retorna objetos date, não datetime
    start_date = pd.to_datetime(data_range[0])
    end_date = pd.to_datetime(data_range[1])

    # Filtra as linhas onde a Data está dentro do intervalo selecionado
    # >= start_date E <= end_date — intervalo fechado nos dois extremos
    filtered_df = filtered_df[
        (filtered_df['Data'] >= start_date) & 
        (filtered_df['Data'] <= end_date)
    ]

    # Filtra por regiões — mantém apenas as linhas com regiões selecionadas
    # O 'if regions' evita filtrar quando a lista estiver vazia
    if regions:
        filtered_df = filtered_df[filtered_df['Região'].isin(regions)]

    # Filtra por produtos — mantém apenas as linhas com produtos selecionados
    # O 'if products' evita filtrar quando a lista estiver vazia
    if products:
        filtered_df = filtered_df[filtered_df['Produto'].isin(products)]

    return filtered_df


# ─── FUNÇÃO: CALCULAR MÉTRICAS ───────────────────────────────────────────────

def calculate_metrics(df):
    """
    Calcula métricas agregadas a partir do DataFrame filtrado.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados filtrados.
    
    Retorna:
    dict: Dicionário contendo as métricas calculadas.
    """

    # Cria um dicionário com as principais métricas do negócio
    metrics = {
        'Total de Receita':      df['Receita'].sum(),    # Soma total da receita no período filtrado
        'Total de Vendas':       df['Vendas'].sum(),     # Soma total das vendas no período filtrado
        'Quantidade Total':      df['Quantidade'].sum(), # Total de unidades vendidas
        'Média de Receita':      df['Receita'].mean(),   # Receita média por transação
        'Número de Transações':  len(df)                 # Total de registros no período filtrado
    }

    return metrics