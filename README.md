# Análise Preditiva de Ações

Este projeto tem como objetivo prever os preços de ações da bolsa de valores utilizando dados históricos. A aplicação é construída com Streamlit, uma biblioteca Python que permite criar aplicações web interativas de forma rápida e fácil. O modelo preditivo utiliza o Prophet, uma ferramenta desenvolvida pelo Facebook para previsões de séries temporais.

## Funcionalidades

- **Carregamento de Dados**: Permite selecionar uma ação da bolsa e carregar dados históricos utilizando a API do yfinance.
- **Visualização de Dados**: Exibe gráficos de fechamento das ações ao longo do tempo.
- **Previsão de Preços**: Utiliza o modelo Prophet para prever o preço das ações para os próximos meses.
- **Interatividade**: Interface amigável e interativa para seleção de ações, datas e meses de previsão.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para desenvolver a aplicação.
- **Streamlit**: Biblioteca para criar interfaces web interativas.
- **yfinance**: API para obter dados históricos de ações.
- **Prophet**: Biblioteca para previsões de séries temporais.
- **Plotly**: Biblioteca para visualização de dados interativos.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu_usuario/nome_do_repositorio.git
   cd nome_do_repositorio
2. Crie um ambiente virtual e ative-o:
python -m venv venv
# No Windows
venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate

## Instalação
streamlit run app.py

## Instalação

.
├── app.py                # Arquivo principal da aplicação
├── logo.webp             # Imagem do logo da aplicação
└── README.md             # Este arquivo



