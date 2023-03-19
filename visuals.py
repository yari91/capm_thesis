from capm_model import *
import plotly.express as px
import seaborn as sns
import matplotlib as plt

# PERFORM DATA SCALING

# Read the Crypto DataFrame and Info

cryptos_df.info()
# cryptos_df.describe().to_csv('data/returns_description.csv')

# Set seaborn plot style

sns.set_style("darkgrid")
plt.rc("figure", figsize=(16, 6))
plt.rc("savefig", dpi=90)
plt.rc("font", family="sans-serif")
plt.rc("font", size=14)


# DATA VISUALIZATION

def interactive_plot(df, title):
    figure = px.line(title=title)
    for i in df.columns:
        figure.add_scatter(x=df.index, y=df[i], name=i)
    figure.show()

# Interactive Plot for Daily Prices of chosen [92] Cryptos
# interactive_plot(daily_returns, 'Log Returns of the available Cryptocurrencies')


# Pie chart of cryptos that confirm the rule
