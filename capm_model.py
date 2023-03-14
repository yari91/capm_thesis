# Import all neccessary packages
from extract_data import *
from builtins import print
from prettytable import from_csv
from arch import arch_model
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib as plt


# RAW DATA MANIPULATION


# Function for Date Range
def getPriceRange(cryptoid, start_date, end_date):
    # import daily data from daily folder
    daily_prices = pd.read_csv('daily/daily_' + cryptoid + '.csv').set_index('Date')
    # set dates
    try:
        ranged_data = daily_prices.loc[start_date:end_date]
    except KeyError:
        print('Prices for id: ' + cryptoid + ' N/A.')
        return

    return ranged_data


# Extract Data

def constructAllPrices():
    daily_prices_df = []
    for x in coins_list:
        daily_prices = pd.read_csv('daily/daily_' + x + '.csv')
        daily_prices.rename(columns={'Price': x}, inplace=True)  # Rename price columns as in daily_.csv
        daily_prices.drop_duplicates(subset="Date", keep=False, inplace=True)
        daily_prices['Date'] = pd.to_datetime(daily_prices['Date'])
        daily_prices_df.append(daily_prices)

    return daily_prices_df


# Concatenate csv Files and Sort by DateTimeIndex

rename_column = [df.set_index('Date') for df in constructAllPrices()]
all_cryptos = (pd.concat(rename_column, axis=1)).sort_index()

# all_cryptos.to_csv('data/all_cryptos_dataset.csv')  # Save in csv (for Appendix)


# EXPLORATORY DATA ANALYSIS

# Drop Missing Values

drop_rows = all_cryptos.dropna(subset=['solana'])  # Investigate dates after Solana's ledger start date
drop_rows_mean = drop_rows.drop(drop_rows.columns[drop_rows.isnull().mean() > 0], axis=1)

print('\n Prices for the following crypto: ', drop_rows.columns[drop_rows.isnull().mean() > 0].tolist(),
      ' are dropped. \n')
# print(cryptos_df)

# Set Date Range For a Period

cryptos_df = drop_rows_mean.loc['2020-04-11':'2022-04-11']


# cryptos_df.to_csv('data/final_cryptos_dataset.csv')  # Save in csv (for Appendix)


# Read the Crypto DataFrame and Info

# cryptos_df.info()
# cryptos_df.describe()


# PERFORM DATA SCALING


# Normalize Prices
def normalize(df):
    x = df.copy()
    for i in x.columns:
        x[i] = (x[i] / x[i][0])
    return


# DATA VISUALIZATION

def interactive_plot(df, title):
    figure = px.line(title=title)
    for i in df.columns:
        figure.add_scatter(x=df.index, y=df[i], name=i)
    figure.show()


# Interactive Plot for Daily Prices of chosen [92] Cryptos

# interactive_plot(cryptos_df, 'Prices')

# Set seaborn plot style

sns.set_style("darkgrid")
plt.rc("figure", figsize=(16, 6))
plt.rc("savefig", dpi=90)
plt.rc("font", family="sans-serif")
plt.rc("font", size=14)

# BUILD MODEL

# Exponential Price Normalization

ln_cryptos_df = cryptos_df.transform(lambda x: np.log(x))


# Function to calculate the Daily Return Rate

def daily_return(df):
    daily_return_df = df.copy()
    for i in df.columns:
        for j in range(1, len(df)):
            daily_return_df[i][j] = ((df[i][j] - df[i][j - 1]) / df[i][j - 1]) * 100
        daily_return_df[i][0] = 0
    return daily_return_df


daily_returns = daily_return(cryptos_df)


# daily_returns.to_csv('data/daily_returns.csv')  # Save in csv (for Appendix)


# CAPM E-GARCH(1,1) MODEL

# Get parameters for all crypto in a Dataframe
def constructEGARCH_1_1():
    params = []
    pvals = []
    for x in daily_returns:
        am = arch_model(daily_returns[x], vol='EGARCH', p=1, q=1, dist='normal')
        garch_output = am.fit(disp="off", show_warning=False)

        with open('results/egarch_1_1/' + x + '_summary.txt', 'w') as rs:
            rs.write(garch_output.summary().as_text())

        # exctract P-values
        f_res_html = garch_output.summary().tables[2].as_html()
        f_trial = pd.read_html(f_res_html, header=0, index_col=0)[0].drop(labels='omega').rename(columns={'P>|t|': x},
                                                                                                 inplace=False)
        # Rename parameter columns with name of crypto
        garch_output = pd.DataFrame(garch_output.params).rename(columns={'params': x}, inplace=False).drop(
            labels=["mu", "omega"])
        params.append(garch_output)

        pvals.append(f_trial[x])

    return [params, pvals]


# CAPM E-GARCH(2,1) MODEL

# Get parameters for all crypto in a Dataframe
# def constructEGARCH_2_1():
#     params = []
#     pvals = []
#     for x in daily_returns:
#         am = arch_model(daily_returns[x], vol='EGARCH', p=2, q=1, dist='normal')
#         garch_output = am.fit(disp="off", show_warning=False)
#
#         with open('results/egarch_2_1' + x + '_summary.txt', 'w') as rs:
#             rs.write(garch_output.summary().as_text())
#
#         # exctract P-values
#         f_res_html = garch_output.summary().tables[2].as_html()
#         f_trial = pd.read_html(f_res_html, header=0, index_col=0)[0].drop(labels='omega').rename(columns={'P>|t|': x},
#                                                                                                  inplace=False)
#
#         # Rename parameter columns with name of crypto
#         garch_output = pd.DataFrame(garch_output.params).rename(columns={'params': x}, inplace=False).drop(
#             labels=["mu", "omega"])
#         params.append(garch_output)
#
#         pvals.append(f_trial[x])
#
#     return [params, pvals]

# Finalize Parameters table for selected cryptos

[res_params_1_1, res_pvals_1_1] = constructEGARCH_1_1()

# Concatenate parameters
concat_params = pd.concat(res_params_1_1, axis=1).T.rename(columns={'alpha[1]': 'alpha', 'beta[1]': 'beta'})

# Refine alpha and beta values that support theory
refined_params = concat_params.query("alpha > 0 and beta > 0 and beta <= 1")

# Concatenate p-values and final parameters table including all values
concat_pvals = pd.concat(res_pvals_1_1, axis=1).T.rename(columns={'alpha[1]': 'P_alpha', 'beta[1]': 'P_beta'})
refined_table = pd.concat([refined_params, concat_pvals], axis=1)

# Place in order the columns
order_params = refined_table[["alpha", "P_alpha", "beta", "P_beta"]].dropna()

# Statistical Significant data
cryptos_params = order_params.query("P_alpha != 0 and P_alpha < 0.05 and P_beta != 0 and P_beta < 0.05")

# # Save final table as .xlsx and .csv
# cryptos_params.to_excel(r'results/tables/egarch_1_1.xlsx', index=True)
cryptos_params.to_csv('results/tables/egarch_1_1.csv', index=True)
#
# with open("results/tables/egarch_1_1.csv") as p:
#     egarch_1_1 = from_csv(p)
print(cryptos_params)

correlation_matrix = daily_returns.corr()
print(sns.heatmap(correlation_matrix))
