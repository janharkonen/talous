import pandas as pd
from pandas import DataFrame, Index

pd.set_option('display.max_columns', None)

class RawData:

    def __init__(self, filename : str) -> None:
        self.filename = filename
        self.df = pd.read_csv(filename)

class RawDataScraper(RawData):
    
    def get_cur(self, cur1 : str, cur2 : str) -> str:
        if (cur1 == 'EUR') and (cur2 != 'EUR'):
            return cur2
        elif (cur1 != 'EUR') and (cur2 == 'EUR'):
            return cur1
        else:
            return 'NaN'

    def get_currency_list(self) -> Index:
        assert isinstance(self.df, DataFrame), "Väärä datatyyppi ##0001"

        df2 = self.df[['Currency','To Currency','Native Amount']]
        df2 = df2[(df2['Currency'] == 'EUR') | (df2['To Currency'] == 'EUR')]
        df2['Actual Currency'] = df2.apply(lambda row: self.get_cur(row['Currency'], row['To Currency']), axis=1)
        df2 = df2[['Actual Currency', 'Native Amount']]
        df3 = df2.groupby(['Actual Currency'], as_index='True')['Native Amount'].sum()
        df4 = df2.groupby(['Actual Currency'], as_index='True')['Native Amount'].count()
        df5 = df4 * df3
        df5 = df5.sort_values(ascending=False)
        df5 = df5.index
        currencylist = df5

        return currencylist
