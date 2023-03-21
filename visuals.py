import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
# from capm_model import daily_returns, cryptos_df


# PERFORM DATA SCALING

# Read the Crypto DataFrame and Info

# cryptos_df.info()
# cryptos_df.describe().to_csv('data/returns_description.csv')


# DATA VISUALIZATION

def interactive_plot(df, title):
    figure = px.line(title=title)
    for f in df.columns:
        figure.add_scatter(x=df.index, y=df[f], name=f)
    figure.show()


# # Interactive Plot for Daily Prices of chosen [92] Cryptos (make sure to un-comment the import statement)
# interactive_plot(daily_returns, 'Log Returns of the available Cryptocurrencies')
# interactive_plot(cryptos_df, 'Prices of the available Cryptocurrencies for 2-year period selected')

# # Pie chart of cryptos that were selected
# dropped_cryptos = drop_rows.columns[drop_rows.isnull().mean() > 0]
#
# # data for pie chart
# dropped_len = len(dropped_cryptos)  # number of excluded cryptos due to missing values
# cryptos_len = len(cryptos_df.columns)  # number of cryptos that are included in the dates selected
# sizes1 = [dropped_len, cryptos_len]
# labels = ['Exluded Cryptos', 'Selected Cryptos']
# explode = (0, 0.1)
#
# plt.style.use('ggplot')
# # plt.title('Crypto distribution')
# # plt.pie(x=sizes1, explode=explode, labels=labels, autopct='%.2f%%', shadow=True, startangle=90)
# # plt.axis('equal')
# # plt.savefig('figures/selected_cryptos_piechart.png')
#
eg11 = pd.read_csv('results/tables/egarch_1_1.csv', index_col=0)
eg12 = pd.read_csv('results/tables/egarch_1_2.csv', index_col=0)
eg21 = pd.read_csv('results/tables/egarch_2_1.csv', index_col=0)
# sizes2 = [cryptos_len, len(eg11)]
# sizes3 = [cryptos_len, len(eg12)]
# sizes4 = [cryptos_len, len(eg21)]
#
# fig, axs = plt.subplots(2, 2)
# axs[0, 0].pie(x=sizes1, explode=(0.2, 0), labels=labels, autopct='%.2f%%', shadow=True, startangle=180)
# axs[0, 0].set_title('Crypto distribution')
# axs[0, 1].pie(x=sizes2, explode=explode, labels=labels, autopct='%.2f%%', shadow=True, startangle=90)
# axs[0, 1].set_title('EGARCH(1,1)')
# axs[1, 0].pie(x=sizes3, explode=explode, labels=labels, autopct='%.2f%%', shadow=True, startangle=90)
# axs[1, 0].set_title('EGARCH(1,2)')
# axs[1, 1].pie(x=sizes4, explode=explode, labels=labels, autopct='%.2f%%', shadow=True, startangle=90)
# axs[1, 1].set_title('EGARCH(2,1)')
#
# # add a line frame between the subplots
# lw = 0.5
# frame1 = plt.Rectangle((0, 0), 1, 1, lw=lw, color='black', fill=False)
# frame2 = plt.Rectangle((0, 0), 1, 1, lw=lw, color='black', fill=False)
# frame3 = plt.Rectangle((0, 0), 1, 1, lw=lw, color='black', fill=False)
# frame4 = plt.Rectangle((0, 0), 1, 1, lw=lw, color='black', fill=False)
#
# fig.add_artist(frame1)
# fig.add_artist(frame2)
# fig.add_artist(frame3)
# fig.add_artist(frame4)
#
# frame1.set_bounds(0, 0.5, 0.5, 0.5)
# frame2.set_bounds(0.5, 0.5, 0.5, 0.5)
# frame3.set_bounds(0, 0, 0.5, 0.5)
# frame4.set_bounds(0.5, 0, 0.5, 0.5)
#
# # # adjust the layout of the subplot grid
# plt.tight_layout()
#
# # save the figure as a PNG file
# plt.savefig('figures/pie_charts.png', dpi=300)
# plt.show()

# Barplot of Cryptocurrencies

# Rename columns
eg11.columns = [f"{col}_eg11" for col in eg11.columns]
eg12.columns = [f"{col}_eg12" for col in eg12.columns]
eg21.columns = [f"{col}_eg21" for col in eg21.columns]

# Concatenate dataframes
proved_cryptos = pd.concat([eg11, eg12, eg21], axis=1)

# Fill missing values with NaN
proved_cryptos = proved_cryptos.reindex(
    index=proved_cryptos.index.union(eg11.index).union(eg12.index).union(eg21.index))

# Prepare the data for plotting
alpha_vals = proved_cryptos[['alpha_eg11', 'alpha_eg12', 'alpha_eg21']]
beta_vals = proved_cryptos[['beta_eg11', 'beta_eg12', 'beta_eg21']]


# Create a function for drawing a barplots
def grouped_barplot(egarchp, data):
    # Set up the bar plot
    fig, ax = plt.subplots(figsize=(15, 6))
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
    plt.show()


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
    fig, ax = plt.subplots(figsize=(16, 9))

    # Horizontal Bar Plot
    ax.barh(data.index, data[parameters])

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
        plt.text(i.get_width() + 0.02, i.get_y() + 0.5,
                 str(round((i.get_width()), 2)),
                 fontsize=10, fontweight='bold',
                 color='grey')

    # Add Plot Title
    ax.set_title('Empirically verified' + parameters.split("_")[0] + '-values', loc='left')
    plt.savefig('figures/'+parameters+'_evc.png')


# verified_barplot('alpha_eg11', malpha_vals)
# verified_barplot('alpha_eg12', malpha_vals)
# verified_barplot('alpha_eg21', malpha_vals)
# verified_barplot('beta_eg11', mbeta_vals)
# verified_barplot('beta_eg12', mbeta_vals)
# verified_barplot('beta_eg21', mbeta_vals)
verified_barplot('alpha_eg11', eg11)  # Create and save figure for alpha values only for EGARCH(1,1)
verified_barplot('beta_eg11', eg11)   # Create and save figure for beta values only for EGARCH(1,1)
