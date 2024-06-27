import pandas as pd
from pandas import DataFrame, Index

pd.set_option('display.max_columns', None)

class CsvToRawDataFrame:

    def __init__(self, filename : str) -> None:
        assert filename[-4:] == '.csv', "Input should be a csv file"
        self.filename = filename
        self.df = pd.read_csv(filename)
        self.df['Timestamp (UTC)'] = pd.to_datetime(self.df['Timestamp (UTC)']) #TODO: tämä laittaa sekunnit nolliksi

class RawDataScraper(RawData):

    def __init__(self, input : str | RawData):
        if isinstance(input, str):
            super().__init__(input)
        elif isinstance(input, RawData):
            self.filename = input.filename
            self.df = input.df
        else:
            raise ValueError("Input must be a string filename or a RawData instance.")

    @classmethod
    def from_base(cls, ARawData : RawData):
        inst = cls.__new__(cls)
        inst.filename = ARawData.filename
        inst.df = ARawData.df
        return inst

    def __get_cur(self, cur1 : str, cur2 : str) -> str:
        if (cur1 == 'EUR') and (cur2 != 'EUR'):
            return cur2
        elif (cur1 != 'EUR') and (cur2 == 'EUR'):
            return cur1
        else:
            return 'NaN'

    def __scrape_currency_list(self) -> Index:
        assert isinstance(self.df, DataFrame), "Väärä datatyyppi ##0001"

        df2 = self.df[['Currency','To Currency','Native Amount']]
        df2 = df2[(df2['Currency'] == 'EUR') | (df2['To Currency'] == 'EUR')]
        df2['Actual Currency'] = df2.apply(lambda row: self.__get_cur(row['Currency'], row['To Currency']), axis=1)
        df2 = df2[['Actual Currency', 'Native Amount']]
        df3 = df2.groupby(['Actual Currency'], as_index='True')['Native Amount'].sum()
        df4 = df2.groupby(['Actual Currency'], as_index='True')['Native Amount'].count()
        df5 = df4 * df3
        df5 = df5.sort_values(ascending=False)
        df5 = df5.index
        currencylist = df5

        return currencylist
    
    def __scrape_year_list(self) -> list:
        assert isinstance(self.df, DataFrame), "Väärä datatyyppi ##0002"    

        self.df['Timestamp (UTC)'] = pd.to_datetime(self.df['Timestamp (UTC)'])
        df2 = self.df['Timestamp (UTC)']
        first_year = df2.iloc[-1].year
        last_year = df2.iloc[0].year
        list = range(first_year,last_year+1,1)
        return list