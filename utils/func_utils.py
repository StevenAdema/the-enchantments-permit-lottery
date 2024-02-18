import PyPDF2
import pandas as pd
from io import StringIO
import re
import numpy as np
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype

class Utils():
    def print_nothing(self):
        print('nothing')

    def read_pdf_to_txt(self, pdf_path, txt_path):
        '''
        Read a PDF file and write the text to a text file

        Args:
        pdf_path (str): The path to the PDF file
        txt_path (str): The path to the text file

        Returns:
        None
        '''
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            with open(txt_path, 'w', encoding='utf-8') as text_file:
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_file.write(text + '\n')
                    else:
                        print(f'Could not extract text from page {pdf_reader.pages.index(page)}')

    def clean_txt_file(self, txt_path):
        '''
        Clean the text file
        1. Remove the '(stock)' string
        2. Replace spaces with underscores in zone names
        3. Write the cleaned text to a new file
        
        Args:
        txt_path (str): The path to the text file to be cleaned

        Returns:
        None

        '''
        replacements = {
            'Core Enchantment Zone': 'Core_Enchantment_Zone',
            'Stuart  Zone': 'Stuart_Zone',
            'Stuart Zone': 'Stuart_Zone',
            'Colchuck Zone': 'Colchuck_Zone',
            'Eightmile/Caroline Zone': 'Eightmile/Caroline_Zone',
            'Snow Zone': 'Snow_Zone',
            ' (stock)': '',
        }
        with open(txt_path, 'r', encoding='utf-8') as file:
            f = file.read()

        for old, new in replacements.items():
            f = f.replace(old, new)

        with open(txt_path, 'w') as file:
            file.write(f)

    def read_txt_to_df(self, txt_path, csv_path=None, save_csv=False):
        '''
        Read a text file and write the contents to a DataFrame

        Args:
        txt_path (str): The path to the text file
        csv_path (str): The path to the CSV file
        save_csv (bool): Whether to save the DataFrame to a CSV file

        Returns:
        DataFrame: The DataFrame containing permit lottery results
        '''
        data = []
        pattern = r'(\d+/\d+/\d+)\s+([A-Za-z_]+)'

        with open(txt_path, 'r') as file:
            for line in file:
                matches = re.findall(pattern, line)
                row = [item for match in matches for item in match]
                while len(row) < 8:
                    row.append(None)
                data.append(row)

        headers = ['application_date', 'zone', 'date_2', 'zone_2', 'date_3', 'zone_3', 'date_awarded', 'zone_awarded']
        df = pd.DataFrame(data, columns=headers)
        
        if save_csv:
            df.to_csv(csv_path, sep='|', index=False)
        
        new_rows_2 = df[['date_2', 'zone_2']].rename(columns={'date_2': 'application_date', 'zone_2': 'zone'})
        new_rows_3 = df[['date_3', 'zone_3']].rename(columns={'date_3': 'application_date', 'zone_3': 'zone'})
        df_appended = df[['application_date', 'zone']].append([new_rows_2, new_rows_3], ignore_index=True)

        df2 = df[['date_awarded', 'zone_awarded']]
        df2 = df2.dropna(subset=['date_awarded'])
        df2 = df2.groupby(['date_awarded', 'zone_awarded'])['zone_awarded'].count().reset_index(name='awarded')

        df = df_appended.groupby(['application_date','zone'])['zone'].count().reset_index(name='applications')

        df = df.merge(df2, how='left', left_on=['application_date', 'zone'], right_on=['date_awarded', 'zone_awarded'])
        df.drop(columns=['date_awarded', 'zone_awarded'], inplace=True)
        df['application_date'] = pd.to_datetime(df['application_date'], errors='coerce')
        df['percentage_awarded'] = 100 * (df['awarded'] / df['applications'])
        df['percentage_awarded'] = df['percentage_awarded'].round(1)

        zone_order = CategoricalDtype(['Eightmile', 'Stuart_Zone', 'Colchuck_Zone', 'Core_Enchantment_Zone', 'Snow_Zone'], ordered=True)
        df['zone'] = df['zone'].astype(zone_order)
        df = df.sort_values(by=['application_date','zone'])

        return df

    def plot_heatmap(self, df):
        '''
        Plot the DataFrame as a heatmap
        
        Args:
        df (DataFrame): The DataFrame to be plotted

        Returns:
        None
        '''
        df['application_date'] = df['application_date'].dt.strftime('%m-%d, %a')
        df.loc[df['percentage_awarded'] == 0.0, 'percentage_awarded'] = 100.0

        df = df.pivot(index='application_date', columns='zone', values='percentage_awarded').fillna(0).reset_index()
        
        plt.figure(figsize=(10, 6))
        # plt.imshow(df.iloc[:, 1:], cmap='CMRmap', aspect='auto')
        plt.imshow(df.iloc[:, 1:], cmap='viridis', aspect='auto')
        plt.colorbar(label='Percentage Awarded')
        plt.yticks(ticks=range(len(df)), labels=df['application_date'])
        plt.xticks(ticks=range(len(df.columns[1:])), labels=df.columns[1:], rotation=45)
        plt.title('Percentage Awarded by Zone and Date')
        plt.xlabel('Zone')
        plt.ylabel('Date')
        plt.clim(0, 20)
        plt.tight_layout()
        plt.show()