# Dashboard de Análise de Vendas

## Sobre o Projeto

Dashboard interativo de análise de vendas desenvolvido com **Python** e **Streamlit**, com dados de 2024 a 2026. Permite visualizar tendências de receita, filtrar por data, região e produto, e exportar os dados filtrados como CSV.

Projeto desenvolvido como capstone do curso de Streamlit, cobrindo desde a geração de dados sintéticos até o deploy de uma aplicação multi-página com configurações persistentes via `session_state`.

---

## Demonstração

Link do projeto em execução: [Dashboard de Vendas](https://projetodashaboardvendas.streamlit.app/)

---

## Estrutura do Projeto

```text
capstone_project/
│
├── data/
│   ├── create_sample_data.py   # Gera os dados sintéticos de 2024 a 2026
│   └── sample_data.csv         # Dataset gerado (1096 registros)
│
├── pages/
│   ├── __init__.py
│   ├── 1_Dashboard.py          # Página de KPIs e gráficos principais
│   ├── 2_Análises.py           # Análises temporais e insights de clientes
│   └── 3_Ferramentas.py        # Upload de dados e configurações
│
├── utils/
│   ├── charts.py               # Funções de criação dos gráficos Plotly
│   └── data_loader.py          # Funções de carga, filtro e métricas
│
├── app.py                      # Página inicial do dashboard
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação completa do projeto

---

## Tecnologias Utilizadas

| Biblioteca | Versão mínima | Uso no projeto |
|------------|---------------|----------------|
| Streamlit | 1.28.0 | Interface web, sidebar, tabs, session\_state |
| Pandas | 2.0.0 | Leitura do CSV, filtros, agrupamentos, resample |
| Plotly | 5.17.0 | Gráficos interativos — linha, barras, pizza, heatmap |
| NumPy | 1.24.0 | Geração de dados aleatórios e cálculos numéricos |
| OpenPyXL | 3.1.0 | Suporte a exportação Excel (uso futuro) |

---

## Funcionalidades

- Filtragem interativa por intervalo de datas, regiões e produtos
- KPIs em tempo real — Total de Receita, Total de Vendas, Média de Receita, Quantidade e Transações
- Gráfico de linha com agrupamento por dia, semana, mês ou trimestre
- Gráfico de pizza/donut de distribuição de receita por região
- Gráfico de barras de vendas por produto
- Mapa de calor de vendas por dia da semana vs mês
- Comparação mensal de receita por ano (2024, 2025, 2026)
- Análise de receita por filipo de cliente (Novo, Recorrente, VIP)
- Formatação de valores monetários no padrão brasileiro (R$ 000.000,00)
- Exportação dos dados filtrados como CSV
- Upload de novos arquivos CSV para substituir o dataset
- Configurações de tema, grid, casas decimais e paginação persistidas via `session_state`

---

## Como Executar

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/capstone_project.git
cd capstone_project
```

**2. Crie e ative o ambiente virtual**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Gere os dados de exemplo
**

```bash
python data/create_sample_data.py
```

**5. Execute o dashboard**

```bash
streamlit run app.py
```

O dashboard estará disponível em `https://projetodashaboardvendas.streamlit.app/`

---

## Páginas do Dashboard

**app.py — Página Inicial** Apresenta o menu de boas-vindas, carrega o dataset e exibe métricas gerais (total de registros, intervalo de datas, regiões e produtos) com prévia dos dados.

**1\_Dashboard.py — Dashboard de Vendas** Filtros na sidebar por data, região e produto. Exibe 5 KPIs e três gráficos: tendência de receita, distribuição por região e vendas por produto. Inclui tabela paginada e botão de download do CSV filtrado.

**2\_Análises.py — Análise Avançada** Três abas: Tendências (agrupamento temporal configurável), Análise Temporal (heatmap + barras por dia da semana + comparação mensal por ano) e Insights dos Clientes (pizza por tipo de cliente, tendência mensal e tabela de métricas).

**3\_Ferramentas.py — Ferramentas e Configurações** Upload de novo CSV, estatísticas da base atual, configurações de tema/grid/casas decimais/paginação salvas no `session_state` e opção de reset.

---

## Arquitetura do Código

| Arquivo | Função principal |
|---------|------------------|
| `utils/data_loader.py` | `load_data()` com cache, `filter_data()` e `calculate_metrics()` |
| `utils/charts.py` | `create_revenue_trend()`, `create_region_pie()`, `create_product_bar()`, `create_heatmap()` |
| `data/create_sample_data.py` | Gera 1096 registros diários de 2024 a 2026 com `numpy` e `pandas` |
| `pages/` | Cada arquivo é uma página do Streamlit carregada automaticamente pelo framework |

---

**Padrões utilizados:**

- Separação entre lógica de dados (`utils/`) e interface (`pages/`)
- Cache com `@st.cache_data` para evitar recarregamento desnecessário do CSV
- `sys.path.append` nas páginas para importar `utils/` corretamente
- Configurações globais persistidas via `st.session_state` entre páginas
- Formatação monetária brasileira via substituição encadeada de separadores

---

## Autor

**Danilo Oliveira dos Santos**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DaniloSantos1985)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/danilo-oliveira-santos-b5b3a1174/)

---

**Licença:** MIT · **Ano:** 2026