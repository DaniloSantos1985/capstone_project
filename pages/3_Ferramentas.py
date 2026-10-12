# ─── IMPORTAÇÕES ────────────────────────────────────────────────────────────────

import streamlit as st                  # Framework para criação da interface web
import pandas as pd                     # Biblioteca pandas
from utils.data_loader import load_data # Função para carregar o CSV

# ─── CONFIGURAÇÃO DA PÁGINA ─────────────────────────────────────────────────────

# Define título da aba do navegador e layout em tela cheia
st.set_page_config(
    page_title='Ferramentas',
    layout='wide'
)

# Título principal e linha divisória
st.title('Ferramentas e Configurações')
st.markdown('---')

# =========================================================================
# SEÇÃO 1 — GERENCIAMENTO DE DADOS
# =========================================================================
st.header('Gerenciamento de Dados')

# Divide a área em 2 colunas de tamanho igual
# col1 → upload de novos dados | col2 → informações da base atual
col1, col2 = st.columns(2)

with col1:
    st.subheader('Upload de Novos Dados')

    # Widget de upload de arquivo — aceita apenas arquivos CSV
    # help → texto de ajuda exibido ao passar o mouse no widget
    uploader_file = st.file_uploader(
        'Escolha um arquivo CSV',
        type=['csv'],
        help='Carregue um novo arquivo de vendas para trocar o dataset atual.'
    )

    if uploader_file is not None:
        try:
            # Lê o arquivo CSV enviado pelo usuário e converte em DataFrame
            new_df = pd.read_csv(uploader_file)

            # st.success() → exibe uma caixa de mensagem verde de sucesso na interface
            # f-string → permite inserir variáveis diretamente dentro da string
            # len(new_df) → conta o número de linhas do DataFrame carregado
            # :, → formata o número com separador de milhar (ex: 1,365 em vez de 1365)
            st.success(f'Arquivo carregado com sucesso! {len(new_df):,} registros encontrados.')

            # st.expander → seção recolhível para pré-visualização dos dados
            with st.expander('Pré-visualização dos dados carregados.'):
                # Exibe as primeiras 5 linhas do DataFrame carregado
                st.dataframe(new_df.head(), use_container_width=True)

            # Botão para salvar o novo CSV substituindo o arquivo atual
            if st.button('Salvar Dados Carregados'):
                # Salva o DataFrame como CSV na pasta data/
                # index=False → não inclui a coluna de índice numérico
                new_df.to_csv('data/sample_sales.csv', index=False)
                st.success('Dados salvos com sucesso! Por favor, recarregue o app para ver as mudanças')

                # Exibe balões na tela
                st.balloons()

        except Exception as e:
            # Exibe mensagem de erro caso o arquivo não possa ser lido
            st.error(f'Erro de leitura do arquivo: {e}')

with col2:
    st.subheader('Informações da Base de Dados atual')

    # Carrega os dados do CSV atual usando cache
    df = load_data()

    if df is not None:
        # Exibe estatísticas da base de dados atual em formato informativo
        # memory_usage(deep=True).sum() → calcula o tamanho total em bytes
        # / 1024 → converte para kilobytes
        st.info(f"""
        **Estatísticas da Base de Dados:**
        - Registros: {len(df):,}
        - Colunas: {len(df.columns)}
        - Intervalo de Datas: {df['Data'].min().strftime('%d-%m-%Y')} até {df['Data'].max().strftime('%d-%m-%Y')}         
        - Tamanho do arquivo: {df.memory_usage(deep=True).sum() / 1024:.2f} KB
        """)

        # Converte o DataFrame para CSV em memória para download
        # index=False → não inclui a coluna de índice numérico
        # .encode('utf-8') → codifica para bytes, necessário para o download
        csv = df.to_csv(index=False).encode('utf-8')

        # Botão de download para baixar o dataset atual como backup        
        st.download_button(
            label='Carregar a Base de Dados Atual',
            data=csv,
            file_name='sales_data_backup.csv',
            mime='text/csv'
        )

st.markdown('---')

# =========================================================================
# SEÇÃO 2 — CONFIGURAÇÕES DE FERRAMENTAS
# =========================================================================
st.header('Configurações de Ferramentas')

# Divide a área em 2 colunas de tamanho igual
# col1 → preferências gráficas | col2 → configurações de exibição
col1, col2 = st.columns(2)

with col1:
    st.subheader('Preferências Gráficas')

    # Selectbox para escolher o tema visual dos gráficos Plotly
    chart_theme = st.selectbox(
        'Temas do gráfico',
        ['plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn'],
        help='Selecione o visual para o tema dos gráficos'
    )

    # Checkbox para exibir ou ocultar linhas de grid nos gráficos
    # value=True → marcado por padrão
    show_grid = st.checkbox('Mostrar Linhas de Grid', value=True)

    # Checkbox para habilitar ou desabilitar animações nos gráficos
    animation_enable = st.checkbox('Animações habilitadas', value=True)

with col2:
    st.subheader('Mostrar Dados')

    # Slider para definir o número de casas decimais exibidas
    # min=0, max=4, default=2
    decimal_places = st.slider('Casas decimais', 0, 4, 2)

    # Selectbox para escolher o formato de exibição das datas
    date_format = st.selectbox(
        'Formatar Data',
        ['%Y-%m-%d', '%m-%d-%Y', '%d-%m-%Y', '%B-%d-%Y']
    )

    # select_slider → slider com valores discretos predefinidos
    # Permite escolher quantas linhas exibir por página nas tabelas
    rows_per_page = st.select_slider(
        'Linhas por página padrão',
        options=[10, 25, 50, 100, 250]
    )

    # Botão para salvar todas as configurações de exibição
    if st.button('Salvar configurações de exibição'):

        # st.session_state → armazena as configurações na sessão do usuário
        # Os valores persistem enquanto o usuário não fechar ou recarregar a página
        st.session_state['chart_theme']       = chart_theme
        st.session_state['show_grid']         = show_grid
        st.session_state['animation_enable']  = animation_enable
        st.session_state['decimal_places']    = decimal_places
        st.session_state['date_format']       = date_format
        st.session_state['rows_per_page']     = rows_per_page

        st.success('Ferramentas salvas com sucesso!')
        st.info('Nota: Algumas ferramentas precisam de atualização da página para ter efeito.')

st.markdown('---')

# =========================================================================
# SEÇÃO 3 — SOBRE O DASHBOARD
# =========================================================================
st.header('Sobre esse Dashboard')

# Exibe informações sobre o projeto em formato Markdown
# Inclui características, tecnologias, autor e licença
st.markdown("""
### Dashboard de Análise de Vendas v1.0

Esse Dashboard foi criado como parte do **Projeto Final Streamlit (Módulo 13)**

**Características:**
- Filtragem interativa de dados
- Cálculo de KPIs em tempo real
- Múltiplos tipos de visualização
- Recursos de análise avançada
- Funcionalidade de importação/exportação de dados
- Configurações de exibição personalizáveis

**Tecnologias utilizadas:**
- Streamlit
- Pandas
- Plotly
- Python 3.x

**Criado por:** Danilo Oliveira dos Santos
**Data:** 2026
**Licença:** MIT

---
**Precisa de ajuda?**
Confira a [Documentação do Streamlit](https://docs.streamlit.io/) para mais informações.
""")

# =========================================================================
# SEÇÃO 4 — RESETAR CONFIGURAÇÕES
# =========================================================================
st.markdown('---')
st.subheader('Resetar para padrão')

# Aviso em amarelo alertando sobre a ação irreversível
st.warning('Esta ação redefinirá todas as configurações e dados para os valores padrão.')

# Botão de reset com estilo secundário (menos destaque visual)
if st.button('Resetar tudo', type='secondary'):

    # Checkbox de confirmação — o usuário deve marcar antes de resetar
    # Evita resets acidentais
    if st.checkbox('Eu entendo que todas as customizações de ferramentas serão apagadas.'):

        # Percorre todas as chaves do session_state e as remove
        # list(...keys()) → cria uma cópia da lista para evitar erro ao deletar durante iteração
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.success('Ferramentas resetadas. Por favor, recarregue a página')