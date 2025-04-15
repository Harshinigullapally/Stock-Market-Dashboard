import plotly.express as px
import pandas as pd

# Sample data for 11 sectors
data = {
    "Sector": [
        "Technology", "Healthcare", "Finance", "Energy", "Consumer Goods",
        "Industrials", "Telecommunications", "Real Estate", "Utilities",
        "Materials", "Transportation"
    ],
    "Value": [
        300, 250, 220, 180, 170,
        160, 140, 130, 120,
        110, 100
    ]
}

df = pd.DataFrame(data)

# Create treemap
fig = px.treemap(df, path=["Sector"], values="Value", title="Market Sectors Treemap")
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

# Show plot
fig.show()
