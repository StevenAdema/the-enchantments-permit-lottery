import PyPDF2
import pandas as pd
from io import StringIO
import re
import matplotlib.pyplot as plt
from utils.func_utils import Utils

pdf_path = '.\\data\\fseprd1162873.pdf'
txt_path = '.\\data\\fseprd1162873.txt'
csv_path = '.\\data\\fseprd1162873.csv'
utils = Utils()

# utils.read_pdf_to_txt(pdf_path, txt_path)
# utils.clean_txt_file(txt_path)
df = utils.read_txt_to_df(txt_path, csv_path, save_csv=True)

# Get only July dates of interest
df = df[(df['application_date'] >= '2023-06-20') & (df['application_date'] <= '2023-07-07')]

# Print heat map of lottery permit day odds
# utils.plot_heatmap(df)

# Print bar plot of lotter permit day odds
# utils.plot_barplot(df)

# Sample lottery selections
lottery_dic = [
        {'date': '2023-06-20', 'zone':'Snow Zone', 'n': 3},
        {'date': '2023-06-21', 'zone':'Snow Zone', 'n': 3},
        {'date': '2023-06-22', 'zone':'Stuart Zone', 'n': 2},
        {'date': '2023-06-20', 'zone':'Core Zone', 'n': 1}
    ]

# Print distribution plot of expected permit odds
utils.plot_distribution(df, lottery_dic, simulations=1000)
