import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_columns', None)


class RawData:


    def __init__(self):
        self.df = pd.DataFrame()

class CsvToRawData(RawData):
    def __init__(self, filename : str) -> None:
        assert filename[-4:] == '.csv', "Input should be a csv file"
        self.filename = filename
        self.df = pd.read_csv(filename)
        self.df['Timestamp (UTC)'] = pd.to_datetime(self.df['Timestamp (UTC)']) #TODO: tämä laittaa sekunnit nolliksi

class RefinedData: 
    def __init__(self, input : CsvToRawData) -> None:
        assert isinstance(input, CsvToRawData), "Input must be an instance of CsvToRawData"
        self.df = self.__convert_rawdata_to_refined(input.df)
        
    def __convert_rawdata_to_refined(self, df_in : DataFrame) -> DataFrame:
        return df_in
