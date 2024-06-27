import pandas as pd
from pandas import DataFrame, Index

pd.set_option('display.max_columns', None)

class CsvToRawDataFrame:

    def __init__(self, filename : str) -> None:
        assert filename[-4:] == '.csv', "Input should be a csv file"
        self.filename = filename
        self.df = pd.read_csv(filename)
        self.df['Timestamp (UTC)'] = pd.to_datetime(self.df['Timestamp (UTC)']) #TODO: tämä laittaa sekunnit nolliksi

class RefinedData: 
    def __init__(self, input : DataFrame) -> None:
        assert isinstance(input, DataFrame), "Input must be an instance of DataFrame"
        self.df = input
        self.__drop_irrelevant_lines()
        self.__extend_lines_with_better_data()
        self.df = self.df

    def __extract_relevant_lines_only(self, ADataFrame, list) -> DataFrame:
        def isOK(AStr : str) -> bool:
            return AStr in list
        return ADataFrame[ADataFrame['Transaction Kind'].apply(isOK)]


    def __drop_irrelevant_lines(self):
        acceptable_transaction_kind = [\
                                        'crypto_earn_interest_paid', \
                                        'referral_card_cashback', \
                                        'mco_stake_reward', \
                                        'finance.lockup.dpos_compound_interest.crypto_wallet', \
                                        'card_cashback_reverted', \
                                        'viban_purchase', \
                                        'crypto_viban_exchange', \
                                        'crypto_purchase'
                                        ]
        self.df = self.__extract_relevant_lines_only(self.df, acceptable_transaction_kind)
    
    def __extend_lines_with_better_data(self):
        self.df = self.df[['Timestamp (UTC)', 'Transaction Description', 'Currency','Amount', 'To Currency','To Amount', 'Native Currency', 'Native Amount','Transaction Kind']]
        self.df = self.df
