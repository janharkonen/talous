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
        
    def __convert_row(self, row):
        row_out = None
        match row['Transaction Kind']:
            case 'crypto_purchase':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'], 
                            'Aikaleima': row['Timestamp (UTC)'], 
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': row['Native Amount'],
                            'Määrä kryptovaluuttana': row['Amount'],
                            'EUR/kryptovaluutta': row['Native Amount']/row['Amount'],
                            'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})

        return row_out

    def __convert_rawdata_to_refined(self, df_in : DataFrame) -> DataFrame:
        out_indexes = [
            'Kryptovaluutta',
            'Aikaleima',
            'Osto/Myynti',
            'Hinta (EUR)',
            'Määrä kryptovaluuttana',
            'EUR/kryptovaluutta',
            'Kryptovaluuttaa jäljellä (FIFO)',
            'Laskettu ostohinta',
            'Voitto',
            'Kommentti'
        ]
        df_out = pd.DataFrame(columns=out_indexes)
        for i, row_in in df_in.reindex().sort_index(ascending=False).iterrows():
            row_out = self.__convert_row(row_in)
            if not row_out is None:
                df_out = pd.concat([df_out, row_out.to_frame().T], ignore_index=True)
        return df_out
