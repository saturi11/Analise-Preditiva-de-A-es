import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from datetime import date
from plotly import graph_objs as go

# Dicionário de tickers e seus respectivos nomes
TICKERS = {
    "PETR4.SA": "Petrobras",
    "ABEV3.SA": "Ambev",
    "MGLU3.SA": "Magazine Luiza",
    "BBAS3.SA": "Banco do Brasil",
    "GOOG": "Google",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
}


# Função para carregar dados das ações
def carrega_dados(ticker, dt_inicial, dt_final):
    df = yf.Ticker(ticker).history(
        start=dt_inicial.strftime("%Y-%m-%d"), end=dt_final.strftime("%Y-%m-%d")
    )
    return df


# Função para prever dados
def prever_dados(df, meses_previsao):
    df.reset_index(inplace=True)
    df = df[["Date", "Close"]]
    df["Date"] = df["Date"].dt.tz_localize(None)
    df.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)

    modelo = Prophet()
    modelo.fit(df)
    futuro = modelo.make_future_dataframe(periods=int(meses_previsao) * 30)
    previsoes = modelo.predict(futuro)
    return modelo, previsoes


# Interface do Streamlit
st.image("logo.webp")
st.title("Análise Preditiva")
st.subheader("Prevendo valor de ações na Bolsa de Valores")

# Menu lateral para seleção de parâmetros
with st.sidebar:
    st.header("Menu")
    ticker = st.selectbox("Selecione a ação:", list(TICKERS.keys()))
    dt_inicial = st.date_input("Data Inicial", value=date(2020, 1, 1))
    dt_final = st.date_input("Data Final", value=date.today())
    meses_previsao = st.number_input("Meses de previsão", 1, 24, value=6)

# Carregar os dados
dados = carrega_dados(ticker, dt_inicial, dt_final)

# Exibir dados e gráficos se houver dados disponíveis
if not dados.empty:
    st.header(f"Dados da ação - {TICKERS[ticker]}")
    st.dataframe(dados)

    st.subheader("Variação no período")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dados.index,
            y=dados["Close"],
            mode="lines",
            name="Fechamento",
            line=dict(color="blue"),
        )
    )
    fig.update_layout(
        title="Fechamento das Ações",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        template="plotly_white",
    )
    st.plotly_chart(fig)

    # Previsão para os próximos meses
    st.header(f"Previsão para o(s) próximo(s) {meses_previsao} mês(es)")
    modelo, previsoes = prever_dados(dados, meses_previsao)

    # Gráfico de previsão com incerteza
    fig_previsao = plot_plotly(modelo, previsoes)
    fig_previsao.update_layout(
        title="Previsão de Preços com Incerteza",
        yaxis_title="Preço (R$)",
        xaxis_title="Data",
    )

    # Adicionar gráfico de dispersão para previsões
    fig_scatter = go.Figure()

    # Gráfico de Fechamento
    fig_scatter.add_trace(
        go.Scatter(
            x=dados["Date"],
            y=dados["Close"],
            mode="lines+markers",
            name="Fechamento",
            line=dict(color="blue"),
        )
    )

    # Gráfico de Previsões
    fig_scatter.add_trace(
        go.Scatter(
            x=previsoes["ds"],
            y=previsoes["yhat"],
            mode="lines",
            name="Previsão",
            line=dict(color="orange"),
        )
    )

    # Adicionar intervalo de confiança
    fig_scatter.add_trace(
        go.Scatter(
            x=previsoes["ds"],
            y=previsoes["yhat_upper"],
            mode="lines",
            name="Limite Superior",
            line=dict(color="red", dash="dash"),
        )
    )
    fig_scatter.add_trace(
        go.Scatter(
            x=previsoes["ds"],
            y=previsoes["yhat_lower"],
            mode="lines",
            name="Limite Inferior",
            line=dict(color="red", dash="dash"),
        )
    )

    fig_scatter.update_layout(
        title="Previsão de Preços com Intervalo de Confiança",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        template="plotly_white",
    )

    st.plotly_chart(fig_scatter)

else:
    st.warning("Nenhum dado encontrado no período selecionado.")
