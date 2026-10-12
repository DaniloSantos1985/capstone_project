# Importação das bibliotecas necessárias
import streamlit as st                       # Framework para criação da interface web
from utils.data_loader import load_data      # Função customizada para carregar os dados do CSV

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────
# Define as configurações globais da página do Streamlit
# page_title            → título exibido na aba do navegador
# layout="wide"         → usa toda a largura da tela
# initial_sidebar_state → sidebar já aberta ao carregar a página
st.set_page_config(
    page_title="Dashboard de Análise de Vendas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── ESTILO CUSTOMIZADO ──────────────────────────────────────────────────────

# Injeta CSS customizado diretamente na página para melhorar a aparência
# unsafe_allow_html=True → necessário para renderizar HTML/CSS no Streamlit
# .main         → reduz o padding lateral da área principal
# .stMetric     → adiciona fundo cinza claro, espaçamento e bordas arredondadas nos cards de métricas
st.markdown("""
<style>
.main {
    padding: 0rem 1rem;
}
.stMetric {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─── CABEÇALHO DA PÁGINA ─────────────────────────────────────────────────────

# Título principal exibido no topo da página
st.title("Dashboard de Análise de Vendas")

# Linha divisória horizontal
st.markdown('---')

# ─── MENU DE BOAS-VINDAS ─────────────────────────────────────────────────────

# Texto introdutório com as funcionalidades do dashboard
# Renderizado em Markdown — suporta títulos, listas e negrito
st.markdown("""
### Bem-vindo ao Dashboard de Análise de Vendas!
Este dashboard permite que você explore e visualize dados de vendas de forma interativa.
- Visualize trends de vendas ao longo do tempo.
- Filtre por datas, regiões e produtos.
- Analise métricas de desempenho.
- Exporte os dados filtrados para análise adicional.

**Vamos começar selecionando uma página na barra lateral!**
""")

# ─── CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────

# st.spinner → exibe um ícone de carregamento enquanto os dados são lidos do CSV
# A função load_data() usa @st.cache_data — após a primeira execução
# os dados ficam em cache e não são recarregados desnecessariamente
with st.spinner('Carregando dados...'):
    df = load_data()

# ─── EXIBIÇÃO DOS DADOS ──────────────────────────────────────────────────────

if df is not None:
    # Exibe mensagem de sucesso com o total de registros carregados
    st.success(f'Dados carregados com sucesso! Total de registros: {len(df)}')

    # Divide a área em 4 colunas com proporções [1, 2, 1, 1]
    # A coluna 2 é maior (proporção 2) para acomodar o intervalo de datas
    col1, col2, col3, col4 = st.columns([1, 1.1, 1, 1])

    with col1:
        # Total de registros formatado com separador de milhar
        st.metric('Total de Registros', f'{len(df):,}'.replace(',','.'))

    with col2:
        # Intervalo de datas — exibe a data mínima e máxima do dataset
        # strftime('%d-%m-%Y') → formata a data no padrão brasileiro DD-MM-AAAA
        st.metric(
            "Intervalo de Datas",
            f"{df['Data'].min().strftime('%d-%m-%y')} até {df['Data'].max().strftime('%d-%m-%y')}"
        )

    with col3:
        # Número de regiões únicas no dataset
        # nunique() → conta valores distintos na coluna
        st.metric('Regiões', df['Região'].nunique())

    with col4:
        # Número de produtos únicos no dataset
        st.metric('Produtos', df["Produto"].nunique())

    # Exibe as primeiras 10 linhas do DataFrame como prévia dos dados
    # ⚠️ width='stretch' não é válido — substituir por use_container_width=True
    st.dataframe(
        df.head(10).style.format({
            "Receita": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        }), 
        use_container_width=True, 
        height=300
    )

else:
    # Exibe mensagem de erro caso o arquivo CSV não seja encontrado ou tenha problema
    st.error('Falha ao carregar os dados. Verifique o arquivo CSV e tente novamente.')

# ─── RODAPÉ ──────────────────────────────────────────────────────────────────

# Linha divisória antes do rodapé
st.markdown('---')

# Rodapé centralizado com HTML customizado
# text-align: center → centraliza o texto
# font-size: 0.9em   → texto levemente menor que o padrão
# color: gray        → cor cinza para o texto
st.markdown("""
<div style="text-align: center; font-size: 0.9em; color: gray;">
    <p>Desenvolvido por Danilo Oliveira dos Santos | Dashboard de Análise de Vendas - 2026</p>
</div>
""", unsafe_allow_html=True)