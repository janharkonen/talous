import pandas as pd
from pandas import DataFrame, Index
#print(__name__)
def get_cur(cur1 : str, cur2 : str) -> str:
    if (cur1 == 'EUR') and (cur2 != 'EUR'):
        return cur2
    elif (cur1 != 'EUR') and (cur2 == 'EUR'):
        return cur1
    else:
        return 'NaN'
def get_currency_list(df : DataFrame) -> Index:
    if not isinstance(df, DataFrame):
        raise TypeError("Verolaskelmat error: df is not DataFrame")

    df2 = df[['Currency','To Currency','Native Amount']]
    df2 = df2[(df2['Currency'] == 'EUR') | (df2['To Currency'] == 'EUR')]
    df2['Actual Currency'] = df2.apply(lambda row: get_cur(row['Currency'], row['To Currency']), axis=1)
    df2 = df2[['Actual Currency', 'Native Amount']]
    df3 = df2.groupby(['Actual Currency'], as_index='True')['Native Amount'].sum()
    df4 = df2.groupby(['Actual Currency'], as_index='True')['Native Amount'].count()
    df5 = df4 * df3
    df5 = df5.sort_values(ascending=False)
    df5 = df5.index
    currencylist = df5
    #currencylist = pd.Series(['BTC','ETH','CRO','DOGE','BNB','ICP','ADA','UNI','LTC','SHIB','XYO','DOT','TGBP','USDC'])

    if not isinstance(currencylist, Index):
        raise TypeError("Verolaskelmat error: currencylist is not Index")
    return currencylist

def get_year_list(df : DataFrame) -> list:
    if not isinstance(df, DataFrame):
        raise TypeError("Verolaskelmat error: df is not DataFrame")

    #TODO: tee funktio joka kaivaa kaikki mahdolliset vuodet df:stä
    df['Timestamp (UTC)'] = pd.to_datetime(df['Timestamp (UTC)'])
    begin = df['Timestamp (UTC)'].iloc[-1]
    end = df['Timestamp (UTC)'].iloc[0]

    yearlist = list(range(begin.year,end.year+1,1))

    if not isinstance(yearlist, list):
        raise TypeError("Verolaskelmat error: currencylist is not list")
    return yearlist

def create_empty_output_DataFrame() -> DataFrame:
    data = {
        'Kryptovaluutta': [],
        'Aikaleima': [],
        'Osto/Myynti': [],
        'Hinta (€)': [],
        'Määrä kryptovaluuttana': [],
        '€ per kryptovaluutta': [],
        'Myymättä jäänyt kryptovaluutta (FIFO)': [],
        'Laskettu ostohinta': [],
        'Voitto': [],
        'Kommenttias': [],
    }

    df = pd.DataFrame(data)
    return df

def parse_currency(input_df : DataFrame, cur : str) -> DataFrame:
    return input_df