import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define stock market sectors
SECTORS = {
    "Consumer Discretionary": ["TSLA", "NKE", "MCD", "AMZN", "HD"],
    "Consumer Staples": ["PG", "KO", "PEP", "WMT", "COST"],
    "Energy": ["XOM", "CVX", "BP", "COP", "SLB"],
    "Financials": ["JPM", "BAC", "GS", "MS", "WFC"],
    "Health Care": ["JNJ", "PFE", "MRNA", "UNH", "ABBV"],
    "Industrials": ["BA", "CAT", "LMT", "UPS", "GE"],
    "Information Technology": ["AAPL", "MSFT", "NVDA", "GOOGL", "META"],
    "Materials": ["BHP", "LIN", "RIO", "FCX", "APD"],
    "Real Estate": ["AMT", "SPG", "PLD", "CBRE", "EQIX"],
    "Telecommunication Services": ["VZ", "T", "TMUS", "CHTR", "CMCSA"],
    "Utilities": ["NEE", "DUK", "SO", "EXC", "AEP"]
}

# Streamlit App Configuration
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Stock Market Dashboard")
st.sidebar.header("📊 Navigation")

# Sidebar navigation
selected_tab = st.sidebar.radio("Select a section:", ["Stock Analysis", "Sector Heatmaps"])

# Timeframe Selection
timeframe = st.sidebar.selectbox("Select Timeframe:", ["6 Months", "1 Week", "6 Years"])

# Map timeframe to yfinance period
period_mapping = {
    "6 Months": "6mo",
    "1 Week": "7d",
    "6 Years": "6y"
}

# Function to fetch stock data
@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_stock_data(symbol, period="6mo"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date  # Convert datetime to date
    return df

if selected_tab == "Stock Analysis":
    st.sidebar.header("📊 Select Sector")

    # Select a sector
    sector = st.sidebar.selectbox("Choose a sector:", list(SECTORS.keys()))

    # Select a stock from the chosen sector
    stock_symbol = st.sidebar.selectbox("Choose a stock:", SECTORS[sector])

    df = get_stock_data(stock_symbol, period_mapping[timeframe])

    if not df.empty:
        # 📊 Display OHLCV Stock Data
        st.subheader(f"📊 {stock_symbol} Stock Price Data - {timeframe}")
        st.dataframe(df[["Date", "Open", "High", "Low", "Close", "Volume"]].tail(10))

        # 📈 Plot Stock Price Line Chart
        fig = px.line(df, x="Date", y="Close", title=f"{stock_symbol} Closing Prices - {timeframe}")
        st.plotly_chart(fig, use_container_width=True)

        # 🏦 Fetch Stock Financial Data
        st.subheader(f"📊 {stock_symbol} Financial Summary")
        
        try:
            stock = yf.Ticker(stock_symbol)
            info = stock.info

            market_cap = info.get("marketCap", "N/A")
            pe_ratio = info.get("trailingPE", "N/A")
            dividend_yield = info.get("dividendYield", "N/A")

            # Display key financial data
            st.write(f"**Market Cap:** ${market_cap:,}" if market_cap != "N/A" else "**Market Cap:** N/A")
            st.write(f"**P/E Ratio:** {pe_ratio}" if pe_ratio != "N/A" else "**P/E Ratio:** N/A")
            st.write(f"**Dividend Yield:** {dividend_yield * 100:.2f}%" if dividend_yield != "N/A" else "**Dividend Yield:** N/A")

        except Exception as e:
            st.error(f"⚠ Error fetching financial data: {e}")

    else:
        st.error("⚠ No data available. Try another stock symbol.")

elif selected_tab == "Sector Heatmaps":
    st.subheader("🔥 Stock Correlation Heatmaps for All Sectors")

    for sector, stocks in SECTORS.items():
        st.markdown(f"### {sector} Sector Heatmap")

        # Fetch historical stock data for all stocks in the sector
        stock_data = {}
        for symbol in stocks:
            df = get_stock_data(symbol, period_mapping[timeframe])
            if not df.empty:
                stock_data[symbol] = df["Close"]

        if stock_data:
            df_corr = pd.DataFrame(stock_data).corr().fillna(0)  # Handle NaN values

            # Create interactive Plotly heatmap
            fig = go.Figure(data=go.Heatmap(
                z=df_corr.values,
                x=df_corr.columns,
                y=df_corr.index,
                colorscale="Viridis",
                hoverongaps=False
            ))

            fig.update_layout(
                title=f"{sector} Sector Stock Correlation Heatmap",
                xaxis_title="Stocks",
                yaxis_title="Stocks"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"⚠ No valid stock data found for {sector}. Try again later.")
