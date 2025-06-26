import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

st.title("Aktienanalyse-Dashboard")

tab1, tab2 = st.tabs(["Einzelaktienanalyse", "Depotanalyse"])

with tab1:
    st.sidebar.header("Aktienauswahl")
    ticker = st.sidebar.text_input(
        "Geben Sie ein Ticker-Symbol ein (z.B. AAPL)", "AAPL"
    ).upper()

    if ticker:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            st.header(f"Informationen für {info.get('longName', ticker)}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Aktueller Preis", f"{info.get('currentPrice', 'N/A'):.2f} USD"
                )
                st.metric("Börsenkapitalisierung", f"{info.get('marketCap', 'N/A'):,}")
            with col2:
                st.metric("Sektor", info.get("sector", "N/A"))
                st.metric("Branche", info.get("industry", "N/A"))
            with col3:
                st.metric("Land", info.get("country", "N/A"))
                st.metric("Website", info.get("website", "N/A"))

            st.subheader("Finanzkennzahlen")
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            with metrics_col1:
                st.metric("KGV (TTM)", f"{info.get('trailingPE', 'N/A'):.2f}")
                st.metric(
                    "Dividendenrendite", f"{info.get('dividendYield', 0):.2f}%"
                )
            with metrics_col2:
                st.metric("Beta", f"{info.get('beta', 'N/A'):.2f}")
                st.metric("EPS (TTM)", f"{info.get('trailingEps', 'N/A'):.2f}")
            with metrics_col3:
                st.metric("Preis/Buchwert", f"{info.get('priceToBook', 'N/A'):.2f}")
                st.metric(
                    "52 Wochen Hoch", f"{info.get('fiftyTwoWeekHigh', 'N/A'):.2f}"
                )
                st.metric("52 Wochen Tief", f"{info.get('fiftyTwoWeekLow', 'N/A'):.2f}")

            st.subheader("Historische Kursentwicklung")
            period = st.sidebar.selectbox(
                "Wählen Sie den Zeitraum:",
                [
                    "1d",
                    "5d",
                    "1mo",
                    "3mo",
                    "6mo",
                    "1y",
                    "2y",
                    "5y",
                    "10y",
                    "ytd",
                    "max",
                ],
                index=3,
            )
            interval = "1d"
            if period == "1d":
                interval = "2m"
            elif period == "5d":
                interval = "15m"

            hist_data = stock.history(period=period, interval=interval)

            if not hist_data.empty:
                fig = go.Figure(
                    data=[
                        go.Candlestick(
                            x=hist_data.index,
                            open=hist_data["Open"],
                            high=hist_data["High"],
                            low=hist_data["Low"],
                            close=hist_data["Close"],
                            name="Kurs",
                        )
                    ]
                )

                fig.update_layout(
                    title_text=f"{ticker} Kursentwicklung",
                    xaxis_rangeslider_visible=False,
                    height=600,
                    xaxis_title="Datum",
                    yaxis_title="Preis",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(
                    "Keine historischen Daten für den ausgewählten Zeitraum verfügbar."
                )

        except Exception as e:
            st.error(f"Fehler beim Abrufen der Daten für {ticker}: {e}")
            st.info(
                "Mögliche Ursachen:\n- Ungültiges Ticker-Symbol.\n- Keine Internetverbindung.\n- API-Ratenbegrenzung überschritten (versuchen Sie es später erneut)."
            )

with tab2:
    st.header("Depotanalyse")
    default_tickers = "AAPL,MSFT,ABNB,ADBE,AMD,AMZN,ASML,BABA,BKNG,BLK,BMY,BRK-B,BTI,BX,COIN,ENPH,GOOGL,GS,JNJ,KO,LMT,MA,META,MDLZ,MMM,NFLX,NVDA,PFE,PLTR,PYPL,SHOP,TTD,TSLA,UBER,UNH,V,VZ,NEE,MO,PM,MCD,JD,PG,VALE,RIO,ABBV,AMGN,UL"
    portfolio_tickers_input = st.text_input(
        "Geben Sie Ticker-Symbole kommagetrennt ein (z.B. AAPL,MSFT)", default_tickers
    ).upper()

    if portfolio_tickers_input:
        tickers_list = [
            ticker.strip()
            for ticker in portfolio_tickers_input.split(",")
            if ticker.strip()
        ]

        if tickers_list:
            portfolio_data = []
            for ticker in tickers_list:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    portfolio_data.append(
                        {
                            "Ticker": ticker,
                            "Name": info.get("longName", "N/A"),
                            "Aktueller Preis (USD)": f"{info.get('currentPrice', 'N/A'):.2f}",
                            "Sektor": info.get("sector", "N/A"),
                            "Branche": info.get("industry", "N/A"),
                            "Land": info.get("country", "N/A"),
                            "KGV (TTM)": f"{info.get('trailingPE', 'N/A'):.2f}",
                            "Dividendenrendite (%)": f"{info.get('dividendYield', 0):.2f}",
                        }
                    )
                except Exception as e:
                    st.warning(f"Konnte Daten für Ticker {ticker} nicht abrufen: {e}")

            if portfolio_data:
                df_portfolio = pd.DataFrame(portfolio_data)
                st.dataframe(df_portfolio, use_container_width=True)
            else:
                st.warning("Keine gültigen Daten für die eingegebenen Ticker gefunden.")
        else:
            st.warning("Bitte geben Sie mindestens ein gültiges Ticker-Symbol ein.")
