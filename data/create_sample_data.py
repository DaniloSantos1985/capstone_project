# Importação das bibliotecas necessárias
import pandas as pd                      # Manipulação de dados e criação do DataFrame
import numpy as np                       # Geração de dados aleatórios

# ─── CONFIGURAÇÃO INICIAL ────────────────────────────────────────────────────

# Define uma semente fixa para o gerador de números aleatórios
# Garante que os dados gerados sejam sempre os mesmos a cada execução
np.random.seed(42)

# Cria uma sequência de datas diárias de 01/01/2024 a 31/12/2026
# freq='D' significa frequência diária — gera 365 datas
dates = pd.date_range(start='2024-01-01', end='2026-12-31', freq='D')

# Armazena o total de registros — será usado como tamanho (size) das colunas
n_records = len(dates)  # 1096 registros (2024 a 2026)

# ─── CRIAÇÃO DOS DADOS ───────────────────────────────────────────────────────

data = {
    # Coluna de datas — uma data por registro, do dia 01/01 ao 31/12
    'Data': dates,

    # Coluna de regiões — escolha aleatória entre 4 regiões para cada registro
    'Região': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], size=n_records),

    # Coluna de produtos — escolha aleatória entre 4 produtos para cada registro
    'Produto': np.random.choice(['Produto A', 'Produto B', 'Produto C', 'Produto D'], size=n_records),

    # Coluna de vendas — valor inteiro aleatório entre R$ 1.000 e R$ 10.000
    'Vendas': np.random.randint(1000, 10000, size=n_records),

    # Coluna de quantidade — número inteiro aleatório entre 10 e 100 unidades
    'Quantidade': np.random.randint(10, 100, size=n_records),

    # Coluna de tipo de cliente — escolha aleatória entre 3 perfis de cliente
    'Tipo_cliente': np.random.choice(['Novo', 'Recorrente', 'VIP'], size=n_records),
}

# ─── CRIAÇÃO DO DATAFRAME ────────────────────────────────────────────────────

# Converte o dicionário em um DataFrame do pandas
df = pd.DataFrame(data)

# ─── COLUNA DE RECEITA ───────────────────────────────────────────────────────

# Calcula a Receita multiplicando Vendas por um fator aleatório entre 1.0 e 1.5
# Simula uma margem de revenda variável — a Receita sempre será maior que as Vendas
# Exemplo: Vendas=5000, fator=1.3 → Receita=6500
df['Receita'] = df['Vendas'] * np.random.uniform(1.0, 1.5, size=n_records)

# ─── EXPORTAÇÃO ──────────────────────────────────────────────────────────────

# Salva o DataFrame como arquivo CSV na pasta 'data/'
# index=False — não inclui a coluna de índice numérico (0, 1, 2...) no arquivo
df.to_csv('data/sample_data.csv', index=False)

# Confirmação no terminal de que o arquivo foi gerado com sucesso
print('Dados de exemplo criados e salvos em "data/sample_data.csv".')