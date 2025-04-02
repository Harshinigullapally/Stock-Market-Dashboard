import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from constant import SECTORS  # Dictionary containing sector-wise stock tickers

# Cache stock data to avoid unnecessary API calls
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_sector_performance_details(sector_stocks):
    performance_data = []
    
    for stock in sector_stocks:
        try:
            ticker = yf.Ticker(stock)
            data = ticker.history(period="1mo")
            if data.empty:
                continue
            
            performance = ((data['Close'][-1] - data['Close'][0]) / data['Close'][0]) * 100
            info = ticker.info
            market_cap = info.get('marketCap', 0)
            
            performance_data.append({
                'Stock': stock,
                'Performance': performance,
                'Market Cap': market_cap,
                'Company Name': info.get('longName', stock),
                'Sector': next((key for key, val in SECTORS.items() if stock in val), "Unknown")
            })
        except Exception as e:
            st.warning(f"Could not fetch data for {stock}: {e}")
    
    return pd.DataFrame(performance_data)

def sector_heatmap(selected_sector):
    if selected_sector == "All Sectors":
        st.header("Stock Market Performance Treemap (All Sectors)")
        
        all_stocks = [stock for sector in SECTORS.values() for stock in sector]
        df = fetch_sector_performance_details(all_stocks)

        if df.empty:
            st.error("No performance data available.")
            return

        fig = px.treemap(
            df, 
            path=['Sector', 'Company Name'],
            values='Market Cap',    
            color='Performance',
            color_continuous_scale='RdYlGn',
            custom_data=['Stock', 'Performance', 'Market Cap']
        )

        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>' +
                          'Stock: %{customdata[0]}<br>' +
                          'Performance: %{customdata[1]:.2f}%<br>' +
                          'Market Cap: $%{customdata[2]:,.0f}<extra></extra>'
        )

        fig.update_layout(
            title='Stock Market Performance Treemap (All Sectors)',
            width=900,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("All Sectors Performance Table")
        df['Performance'] = df['Performance'].apply(lambda x: f"{x:.2f}%")
        df['Market Cap'] = df['Market Cap'].apply(lambda x: f"${x:,.0f}")
        df = df[['Sector', 'Stock', 'Company Name', 'Performance', 'Market Cap']]
        st.dataframe(df, use_container_width=True)
    
    else:
        st.header(f"{selected_sector} Sector Performance Treemap")

        sector_stocks = SECTORS.get(selected_sector, [])
        df = fetch_sector_performance_details(sector_stocks)

        if df.empty:
            st.error(f"No performance data available for {selected_sector} sector.")
            return

        fig = px.treemap(
            df, 
            path=['Company Name'],
            values='Market Cap',    
            color='Performance',
            color_continuous_scale='RdYlGn',
            custom_data=['Stock', 'Performance', 'Market Cap']
        )

        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>' +
                          'Stock: %{customdata[0]}<br>' +
                          'Performance: %{customdata[1]:.2f}%<br>' +
                          'Market Cap: $%{customdata[2]:,.0f}<extra></extra>'
        )

        fig.update_layout(
            title=f'{selected_sector} Sector Performance Treemap',
            width=800,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"{selected_sector} Sector Performance Table")
        df['Performance'] = df['Performance'].apply(lambda x: f"{x:.2f}%")
        df['Market Cap'] = df['Market Cap'].apply(lambda x: f"${x:,.0f}")
        df = df[['Stock', 'Company Name', 'Performance', 'Market Cap']]
        st.dataframe(df, use_container_width=True)

# Ensure session state resets correctly
if "selected_sector" not in st.session_state:
    st.session_state["selected_sector"] = "All Sectors"

# Sidebar Selection
st.sidebar.title("Sector Selection")
sector_list = ["All Sectors"] + list(SECTORS.keys())
selected_sector = st.sidebar.selectbox("Select a sector:", sector_list, index=sector_list.index(st.session_state["selected_sector"]))

# If user selects the same sector, force reload
if st.session_state["selected_sector"] != selected_sector:
    st.session_state["selected_sector"] = selected_sector
    st.experimental_rerun()

# Display the heatmap
sector_heatmap(selected_sector)

