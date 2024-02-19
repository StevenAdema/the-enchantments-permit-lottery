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

# Get only July dates
# df = df[(df['application_date'] >= '2023-05-15') & (df['application_date'] <= '2023-07-31')]
# df = df[(df['application_date'] >= '2023-08-01') & (df['application_date'] <= '2023-10-31')]
df = df[(df['application_date'] >= '2023-07-22') & (df['application_date'] <= '2023-07-28')]

# Print heat map of lottery permit results
utils.plot_heatmap(df)

