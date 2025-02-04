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

    def read_txt_to_df(self, txt_path, csv_path=None, save_csv=False):
        '''
        Read a txt file that is comma separated and write the contents to a DataFrame
        
        Args:
        txt_path (str): The path to the text file
        csv_path (str): The path to save the CSV file (optional)
        save_csv (bool): Whether to save the DataFrame to a CSV file

        Returns:
        DataFrame: The DataFrame containing the data from the text file
        '''
        with open(txt_path, 'r', encoding='utf-8') as file:
            data = file.read()
        
        # Convert the text data to a DataFrame
        df = pd.read_csv(StringIO(data), sep=',')
        
        if save_csv and csv_path:
            df.to_csv(csv_path, index=False)
        
        return df
        

    def clean_zones(self, df):
        '''
        Clean the dataframe using replacement dictionary for values in the 'zone' column
        
        Args:
        df (DataFrame): The DataFrame to be cleaned

        Returns:
        DataFrame: The cleaned DataFrame
        '''
        dict_replace = {
            'Core Enchantment Zone': 'Core Enchantment Zone',
            'Stuart  Zone': 'Stuart Zone',
            'Colchuck Zone': 'Colchuck Zone',
            'Eightmile/Caroline Zone': 'Eightmile Zone',
            'Snow Zone': 'Snow Zone'
        }
        df['zone'] = df['zone'].astype('category')
        df['zone'] = df['zone'].cat.rename_categories(dict_replace)
        df['percentage_awarded'] = df['percentage_awarded'].replace('',0).fillna(0)
        return df
    
    def shift_dates(self, df, date_col, shift):
        '''
        Shift the dates in a DataFrame by a specified number of days
        
        Args:
        df (DataFrame): The DataFrame to be shifted
        date_col (str): The column containing the dates
        shift (int): The number of days to shift the dates

        Returns:
        DataFrame: The shifted DataFrame
        '''
        df[date_col] = pd.to_datetime(df[date_col]) + pd.DateOffset(days=shift)
        return df

    def read_csv_to_df(self, csv_path_input=None, csv_path_output=None, save_csv=False):
        '''
        Read a text file and write the contents to a DataFrame

        Args:
        csv_path (str): The path to the CSV file
        save_csv (bool): Whether to save the DataFrame to a CSV file

        Returns:
        DataFrame: The DataFrame containing permit lottery results
        '''
        df = pd.read_csv(csv_path_input)
        
        if save_csv:
            df.to_csv(csv_path_output, index=False)
        
        df = df.rename({
            'Preferred Entry Date 1': 'application_date', 
            'Preferred Division 1': 'zone', 
            'Awarded Entry Date':'date_awarded',
            'Awarded Entrance Code/Name':'zone_awarded'
            }, axis=1)
        new_rows_2 = df[['Preferred Entry Date 2', 'Preferred Division 2']].rename(columns={'Preferred Entry Date 2': 'application_date', 'Preferred Division 2': 'zone'})
        new_rows_3 = df[['Preferred Entry Date 3', 'Preferred Division 3']].rename(columns={'Preferred Entry Date 3': 'application_date', 'Preferred Division 3': 'zone'})
        df_appended = pd.concat([df[['application_date', 'zone']], new_rows_2, new_rows_3], ignore_index=True)

        df2 = df[['date_awarded', 'zone_awarded']]
        df2 = df2.dropna(subset=['date_awarded'])
        df2 = df2.groupby(['date_awarded', 'zone_awarded'])['zone_awarded'].count().reset_index(name='awarded')

        df = df_appended.groupby(['application_date','zone'])['zone'].count().reset_index(name='applications')

        df = df.merge(df2, how='left', left_on=['application_date', 'zone'], right_on=['date_awarded', 'zone_awarded'])
        df.drop(columns=['date_awarded', 'zone_awarded'], inplace=True)
        df['application_date'] = pd.to_datetime(df['application_date'], errors='coerce')
        df['percentage_awarded'] = 100 * (df['awarded'] / df['applications'])
        df['percentage_awarded'] = df['percentage_awarded'].round(1)

        zone_order = CategoricalDtype(['Eightmile/Caroline Zone', 'Stuart  Zone', 'Colchuck Zone', 'Core Enchantment Zone', 'Snow Zone'], ordered=True)
        df['zone'] = df['zone'].astype(zone_order)
        df = df.sort_values(by=['application_date','zone'])

        if save_csv:
            df.to_csv(csv_path_output, sep='|', index=False)

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
        df.to_csv('./data/pivot_table.csv', sep='|', index=False)
        # df = df.drop(columns=['Colchuck Zone', 'Core Enchantment Zone', 'Eightmile Zone'])

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

    def plot_barplot(self, df):
        '''
        Plot the DataFrame as a bar plot
        
        Args:
        df (DataFrame): The DataFrame to be plotted

        Returns:
        None
        '''
        df['application_date'] = df['application_date'].dt.strftime('%m-%d, %a')
        df.loc[df['percentage_awarded'] == 0.0, 'percentage_awarded'] = 100.0

        df = df.pivot(index='application_date', columns='zone', values='percentage_awarded').fillna(0).reset_index()
        df.to_csv('./data/pivot_t.csv', sep='|', index=False)
        # df = df.drop(columns=['Colchuck_Zone', 'Core_Enchantment_Zone', 'Eightmile'])

        # create a bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, zone in enumerate(df.columns[1:]):
            ax.bar(df['application_date'], df[zone], label=zone, alpha=0.7)

        # show plot legend
        ax.legend()
        plt.show()

    def plot_distribution(self, df, lottery_dic, simulations=1000):
        '''
        Plot the distribution of the expected permit odds
        
        Args:
        df (DataFrame): The DataFrame to be plotted
        
        Returns:
        None
        '''
        # Find odds to each date & zone in lottery_dic
        for lottery in lottery_dic:
            zone_prefix = lottery['zone'][:3]
            matching_rows = df[(df['application_date'] == lottery['date']) & (df['zone'].str.startswith(zone_prefix))]
            if not matching_rows.empty:
                lottery['odds'] = matching_rows.iloc[0]['percentage_awarded']/100
            else:
                lottery['odds'] = None 
    
            lottery['name'] = lottery['date'] + " " + lottery['zone']
        
        outcome_df = pd.DataFrame(columns=[lottery['name'] for lottery in lottery_dic])

        # Simulate the lotteries n times
        for _ in range(simulations):
            run_outcomes = {}
            for lottery in lottery_dic:
                # Simulate each lottery once per run
                if lottery['odds'] is not None:
                    wins = np.random.binomial(n=lottery['n'], p=lottery['odds'])
                else:
                    wins = 0
                run_outcomes[lottery['name']] = wins
            # Append the outcomes of this run to the DataFrame
            outcome_df = pd.concat([outcome_df, pd.DataFrame([run_outcomes])], ignore_index=True)

        outcome_df['Total Wins'] = outcome_df.sum(axis=1)

        # create a plot of the number of occurences in outcome_df['Total Wins']
        plt.hist(outcome_df['Total Wins'], bins=range(0, 6))
        plt.title('Outcomes from {simulations} simulations'.format(simulations=simulations))
        plt.xlabel('Permits Awarded')
        plt.ylabel('Frequency')
        plt.xlim(0, 5)
        plt.xticks(range(0, 5))

        # shift x-axis labels to center over bars
        locs, labels = plt.xticks()
        shift = 0.5
        new_locs = [loc + shift for loc in locs]
        plt.xticks(new_locs, [0,1,2,3,4])

        # add label with bar values
        for i, v in enumerate(outcome_df['Total Wins'].value_counts().sort_index()):
            plt.text(i, v, str(v), ha='left', va='bottom')

        n, bins, patches = plt.hist(outcome_df['Total Wins'], bins=range(0, 6), edgecolor='black')
        for patch, left_edge in zip(patches, bins[:-1]):
            if left_edge == 0:
                patch.set_facecolor('salmon')
            else:
                patch.set_facecolor('lightblue')

        plt.show()