import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from model import daily_returns, cryptos_df, ln_cryptos_df, drop_rows

# PERFORM DATA SCALING

# Read the Crypto DataFrame and Info

cryptos_df.info()
cryptos_df.describe().to_csv('data/returns_description.csv')


# DATA VISUALIZATION

def interactive_plot(df, title):
    figure = px.line(title=title)
    for f in df.columns:
        figure.add_scatter(x=df.index, y=df[f], name=f)
    figure.show()


# # Interactive Plot for Daily Prices of chosen [92] Cryptos (make sure to un-comment the import statement)
# interactive_plot(daily_returns, 'Daily Returns of the available Cryptocurrencies')
# interactive_plot(cryptos_df, 'Prices of the available Cryptocurrencies for 2-year period selected')
# interactive_plot(ln_cryptos_df, 'Log Returns of the available Cryptocurrencies')

# # Pie chart of cryptos that were selected
dropped_cryptos = drop_rows.columns[drop_rows.isnull().mean() > 0]

# data for pie chart
dropped_len = len(dropped_cryptos)  # number of excluded cryptos due to missing values
cryptos_len = len(cryptos_df.columns)  # number of cryptos that are included in the dates selected
sizes1 = [dropped_len, cryptos_len]
labels = ['Exluded Cryptos', 'Selected Cryptos']
explode = (0, 0.1)

plt.style.use('ggplot')
plt.title('Crypto distribution')
plt.pie(x=sizes1, explode=explode, labels=labels, autopct='%.2f%%', shadow=True, startangle=90)
plt.axis('equal')
# # plt.savefig('figures/selected_cryptos_piechart.png')
#
eg11 = pd.read_csv('results/tables/egarch_1_1.csv', index_col=0)
eg12 = pd.read_csv('results/tables/egarch_1_2.csv', index_col=0)
eg21 = pd.read_csv('results/tables/egarch_2_1.csv', index_col=0)
sizes2 = [cryptos_len - len(eg11), len(eg11)]
sizes3 = [cryptos_len - len(eg12), len(eg12)]
sizes4 = [cryptos_len - len(eg21), len(eg21)]

fig, axs = plt.subplots(2, 2)
axs[0, 0].pie(x=sizes1, explode=(0.2, 0), autopct='%.2f%%', shadow=True, startangle=180)
axs[0, 0].set_title('Crypto distribution')
axs[0, 1].pie(x=sizes2, explode=explode, autopct='%.2f%%', shadow=True, startangle=90)
axs[0, 1].set_title('EGARCH(1,1)')
axs[1, 0].pie(x=sizes3, explode=explode, autopct='%.2f%%', shadow=True, startangle=90)
axs[1, 0].set_title('EGARCH(1,2)')
axs[1, 1].pie(x=sizes4, explode=explode, autopct='%.2f%%', shadow=True, startangle=90)
axs[1, 1].set_title('EGARCH(2,1)')

plt.legend(labels, loc='lower center', ncol=2, bbox_to_anchor=(-0.5, -0.3))
# save the figure as a PNG file
plt.savefig('figures/pie_charts.png', dpi=300)

# Barplot of Cryptocurrencies

# Rename columns
eg11.columns = [f"{col}_eg11" for col in eg11.columns]
eg12.columns = [f"{col}_eg12" for col in eg12.columns]
eg21.columns = [f"{col}_eg21" for col in eg21.columns]

# Concatenate dataframes
proved_cryptos = pd.concat([eg11, eg12, eg21], axis=1)
# proved_cryptos.to_csv('results/empirically_valid_results.csv')

# Fill missing values with NaN
proved_cryptos = proved_cryptos.reindex(
    index=proved_cryptos.index.union(eg11.index).union(eg12.index).union(eg21.index))

# Prepare the data for plotting
alpha_vals = proved_cryptos[['alpha_eg11', 'alpha_eg12', 'alpha_eg21']]
beta_vals = proved_cryptos[['beta_eg11', 'beta_eg12', 'beta_eg21']]


# Create a function for drawing a barplots
def grouped_barplot(egarchp, data):
    # Set up the bar plot
    fg, ax = plt.subplots(figsize=(15, 6))
    bar_width = 0.3
    opacity = 0.8

    # ALPHA VALUES PLOT

    # Define colors legend labels for each EGARCH model
    colors = {egarchp + '_eg11': 'b', egarchp + '_eg12': 'r', egarchp + '_eg21': 'g'}
    legend_labels = {egarchp + '_eg11': 'EGARCH(1,1)', egarchp + '_eg12': 'EGARCH(1,2)',
                     egarchp + '_eg21': 'EGARCH(2,1)'}

    # Plot bars for each EGARCH model
    for i, col in enumerate(data.columns):
        ax.bar(np.arange(len(data.index)) + i * bar_width, data[col], width=bar_width, alpha=opacity,
               color=colors[col], label=legend_labels[col])

    # Set up x-axis ticks and labels
    ax.set_xticks(np.arange(len(data.index)) + bar_width)
    ax.set_xticklabels(data.index, rotation=45, ha='right')

    # Add labels and legend
    ax.set_xlabel('Cryptocurrency')
    ax.set_ylabel(egarchp.capitalize() + ' Values')
    ax.set_title(egarchp.capitalize() + ' Values by Crypto and EGARCH')
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.savefig('figures/grouped_' + egarchp + '_values.png', dpi=300, bbox_inches='tight')


# grouped_barplot('alpha', alpha_vals)
# grouped_barplot('beta', beta_vals)

# Barplot for verified cryptos

# Concatenate dataframes and drop NA values
merged_cryptos = pd.concat([eg11, eg12, eg21], axis=1).dropna()

# Prepare the data for plotting
malpha_vals = merged_cryptos[['alpha_eg11', 'alpha_eg12', 'alpha_eg21']]
mbeta_vals = merged_cryptos[['beta_eg11', 'beta_eg12', 'beta_eg21']]


def verified_barplot(parameters, data):
    # Figure Size
    figr, ax = plt.subplots(figsize=(18, 12))

    # Horizontal Bar Plot
    ax.barh(data.index, data[parameters], color='blue', height=0.2)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    ax.grid(b=True, color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.5)

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width() + 0.02, i.get_y() + 0.45,
                 str(round((i.get_width()), 2)),
                 fontsize=10, fontweight='bold',
                 color='grey')

    # Add Plot Title
    ax.set_title('Empirically verified ' + parameters.split("_")[0] + '-values exclusively for EGARCH(2,1)',
                 loc='left')
    plt.savefig('figures/' + parameters + '_egarch_2_1.png')


# verified_barplot('alpha_eg21', eg21)
