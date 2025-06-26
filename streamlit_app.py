import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

st.title("Aktienanalyse-Dashboard")

# Sidebar für Ticker-Eingabe
st.sidebar.header("Aktienauswahl")
ticker = st.sidebar.text_input("Geben Sie ein Ticker-Symbol ein (z.B. AAPL)", "AAPL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Grundlegende Informationen
        st.header(f"Informationen für {info.get('longName', ticker)}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Aktueller Preis", f"{info.get('currentPrice', 'N/A'):.2f} USD")
            st.metric("Börsenkapitalisierung", f"{info.get('marketCap', 'N/A'):,}")
        with col2:
            st.metric("Sektor", info.get('sector', 'N/A'))
            st.metric("Branche", info.get('industry', 'N/A'))
        with col3:
            st.metric("Land", info.get('country', 'N/A'))
            st.metric("Website", info.get('website', 'N/A'))

        st.subheader("Finanzkennzahlen")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        with metrics_col1:
            st.metric("KGV (TTM)", f"{info.get('trailingPE', 'N/A'):.2f}")
            st.metric("Dividendenrendite", f"{info.get('dividendYield', 0) * 100:.2f}%")
        with metrics_col2:
            st.metric("Beta", f"{info.get('beta', 'N/A'):.2f}")
            st.metric("EPS (TTM)", f"{info.get('trailingEps', 'N/A'):.2f}")
        with metrics_col3:
            st.metric("Preis/Buchwert", f"{info.get('priceToBook', 'N/A'):.2f}")
            st.metric("52 Wochen Hoch", f"{info.get('fiftyTwoWeekHigh', 'N/A'):.2f}")
            st.metric("52 Wochen Tief", f"{info.get('fiftyTwoWeekLow', 'N/A'):.2f}")

        # Historische Daten und Chart
        st.subheader("Historische Kursentwicklung")
        period = st.sidebar.selectbox(
            "Wählen Sie den Zeitraum:",
            ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
            index=3 # default to 3mo
        )
        interval = "1d"
        if period == "1d":
            interval = "2m" # 2-minute interval for 1 day
        elif period == "5d":
            interval = "15m" # 15-minute interval for 5 days
        
        hist_data = stock.history(period=period, interval=interval)

        if not hist_data.empty:
            # Candlestick Chart
            fig = go.Figure(data=[go.Candlestick(
                x=hist_data.index,
                open=hist_data['Open'],
                high=hist_data['High'],
                low=hist_data['Low'],
                close=hist_data['Close'],
                name='Kurs'
            )])

            fig.update_layout(
                title_text=f"{ticker} Kursentwicklung",
                xaxis_rangeslider_visible=False,
                height=600,
                xaxis_title="Datum",
                yaxis_title="Preis"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Keine historischen Daten für den ausgewählten Zeitraum verfügbar.")

    except Exception as e:
        st.error(f"Fehler beim Abrufen der Daten für {ticker}: {e}")
        st.info("Mögliche Ursachen:\n- Ungültiges Ticker-Symbol.\n- Keine Internetverbindung.\n- API-Ratenbegrenzung überschritten (versuchen Sie es später erneut).")
