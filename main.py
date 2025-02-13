import PyPDF2
import pandas as pd
from io import StringIO
import re
import matplotlib.pyplot as plt
from utils.func_utils import Utils

txt_path = './data/fseprd1162873.txt'
csv_path = './data/fseprd1162873.csv'
csv_path_2024 = './data/2024_lottery.csv'
csv_path_2025 = './data/2025_lottery.csv'
utils = Utils()

df = utils.read_txt_to_df(txt_path, csv_path, save_csv=True)
df = utils.read_csv_to_df(csv_path_input=csv_path, csv_path_output=csv_path_2024, save_csv=True)

df = utils.clean_zones(df)
df = utils.shift_dates(df,'application_date',364)
df.to_csv(csv_path_2025, index=False)

# Get only July dates of interest
# df = df[(df['application_date'] >= '2025-07-20') & (df['application_date'] <= '2025-07-25')]

# Print heat map of lottery permit day odds
# utils.plot_heatmap(df)

# Print bar plot of lotter permit day odds
utils.plot_barplot(df)

# Sample lottery selections
# lottery_dic = [
#         {'date': '2025-07-20', 'zone':'Snow Zone', 'n': 1},
#         {'date': '2025-07-21', 'zone':'Snow Zone', 'n': 1},
#         {'date': '2025-07-22', 'zone':'Stuart Zone', 'n': 1}
#     ]

# Print distribution plot of expected permit odds
# utils.plot_distribution(df, lottery_dic, simulations=1000)
