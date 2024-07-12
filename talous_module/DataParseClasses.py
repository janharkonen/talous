import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_columns', None)


class RawData:

    def __init__(self):
        self.df = pd.DataFrame()


class CsvToRawData(RawData):

    def __init__(self, filename: str) -> None:
        assert filename[-4:] == '.csv', "Input should be a csv file"
        self.filename = filename
        self.df = pd.read_csv(filename)
        self.df['Timestamp (UTC)'] = pd.to_datetime(self.df['Timestamp (UTC)'])  # TODO: tämä laittaa sekunnit nolliksi


class RefinedData:

    def __init__(self, input: CsvToRawData) -> None:
        assert isinstance(input, CsvToRawData), "Input must be an instance of CsvToRawData"
        self.df = self.__convert_rawdata_to_refined(input.df)
        self._calculate_fifo_and_profit()
        #self.refined_data_by_currency_list = self.__create_refined_data_by_currency_list()

    def __convert_rawdata_to_refined(self, df_in: DataFrame) -> DataFrame:
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
            if row_out is not None:
                df_out = pd.concat([df_out, row_out.to_frame().T], ignore_index=True)
        return df_out

    def __convert_row(self, row):
        row_out = None
        # crypto_purchase
        # viban_purchase
        # #crypto_transfer
        # crypto_viban_exchange
        # card_top_up
        # #referral_gift
        # crypto_earn_interest_paid
        # referral_card_cashback
        # mco_stake_reward
        # #referral_bonus
        # card_cashback_reverted
        # #admin_wallet_credited
        # finance.lockup.dpos_compound_interest.crypto_wallet
        # finance.dpos.compound_interest.crypto_wallet
        # finance.crypto_earn.loyalty_program_extra_interest_paid.crypto_wallet
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
            case 'viban_purchase':
                row_out = pd.Series({
                            'Kryptovaluutta': row['To Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': row['Native Amount'],
                            'Määrä kryptovaluuttana': row['To Amount'],
                            'EUR/kryptovaluutta': row['Native Amount']/row['To Amount'],
                            'Kryptovaluuttaa jäljellä (FIFO)': row['To Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            # case 'crypto_transfer':
            #    row_out = pd.Series({
            #                'Kryptovaluutta': row['Currency'],
            #                'Aikaleima': row['Timestamp (UTC)'],
            #                'Osto/Myynti': 'GIFT',
            #                'Hinta (EUR)': row['Native Amount'],
            #                'Määrä kryptovaluuttana': row['Amount'],
            #                'EUR/kryptovaluutta': row['Native Amount']/row['Amount'],
            #                'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
            #                'Laskettu ostohinta': '',
            #                'Voitto': '',
            #                'Kommentti': ''})
            case 'crypto_viban_exchange':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'SELL',
                            'Hinta (EUR)': row['Native Amount'],
                            'Määrä kryptovaluuttana': -row['Amount'],
                            'EUR/kryptovaluutta': row['Native Amount']/-row['Amount'],
                            'Kryptovaluuttaa jäljellä (FIFO)': 0.0,
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            case 'card_top_up':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'SELL',
                            'Hinta (EUR)': -row['Native Amount'],
                            'Määrä kryptovaluuttana': -row['Amount'],
                            'EUR/kryptovaluutta': -row['Native Amount']/-row['Amount'],
                            'Kryptovaluuttaa jäljellä (FIFO)': 0.0,
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            # case 'referral_gift':
            #    row_out = pd.Series({
            #                'Kryptovaluutta': row['Currency'],
            #                'Aikaleima': row['Timestamp (UTC)'],
            #                'Osto/Myynti': 'GIFT',
            #                'Hinta (EUR)': row['Native Amount'],
            #                'Määrä kryptovaluuttana': row['Amount'],
            #                'EUR/kryptovaluutta': row['Native Amount']/row['Amount'],
            #                'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
            #                'Laskettu ostohinta': '',
            #                'Voitto': '',
            #                'Kommentti': ''})
            case 'crypto_earn_interest_paid':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': 0.0,
                            'Määrä kryptovaluuttana': row['Amount'],
                            'EUR/kryptovaluutta': 0.0,
                            'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            case 'referral_card_cashback':
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
            case 'mco_stake_reward':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': 0.0,
                            'Määrä kryptovaluuttana': row['Amount'],
                            'EUR/kryptovaluutta': 0.0,
                            'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            # case 'referral_bonus':
            #    row_out = pd.Series({
            #                'Kryptovaluutta': row['Currency'],
            #                'Aikaleima': row['Timestamp (UTC)'],
            #                'Osto/Myynti': 'GIFT',
            #                'Hinta (EUR)': row['Native Amount'],
            #                'Määrä kryptovaluuttana': row['Amount'],
            #                'EUR/kryptovaluutta': row['Native Amount']/row['Amount'],
            #                'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
            #                'Laskettu ostohinta': '',
            #                'Voitto': '',
            #                'Kommentti': ''})
            case 'card_cashback_reverted':
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
            # case 'admin_wallet_credited':
            #    row_out = pd.Series({
            #                'Kryptovaluutta': row['Currency'],
            #                'Aikaleima': row['Timestamp (UTC)'],
            #                'Osto/Myynti': 'GIFT',
            #                'Hinta (EUR)': row['Native Amount'],
            #                'Määrä kryptovaluuttana': row['Amount'],
            #                'EUR/kryptovaluutta': row['Native Amount']/row['Amount'],
            #                'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
            #                'Laskettu ostohinta': '',
            #                'Voitto': '',
            #                'Kommentti': ''})
            case 'finance.lockup.dpos_compound_interest.crypto_wallet':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': 0.0,
                            'Määrä kryptovaluuttana': row['Amount'],
                            'EUR/kryptovaluutta': 0.0,
                            'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            case 'finance.dpos.compound_interest.crypto_wallet':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': 0.0,
                            'Määrä kryptovaluuttana': row['Amount'],
                            'EUR/kryptovaluutta': 0.0,
                            'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            case 'reward.loyalty_program.trading_rebate.crypto_wallet':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': 0.0,
                            'Määrä kryptovaluuttana': row['Amount'],
                            'EUR/kryptovaluutta': 0.0,
                            'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})
            case 'finance.crypto_earn.loyalty_program_extra_interest_paid.crypto_wallet':
                row_out = pd.Series({
                            'Kryptovaluutta': row['Currency'],
                            'Aikaleima': row['Timestamp (UTC)'],
                            'Osto/Myynti': 'BUY',
                            'Hinta (EUR)': 0.0,
                            'Määrä kryptovaluuttana': row['Amount'],
                            'EUR/kryptovaluutta': 0.0,
                            'Kryptovaluuttaa jäljellä (FIFO)': row['Amount'],
                            'Laskettu ostohinta': '',
                            'Voitto': '',
                            'Kommentti': ''})

        return row_out

    def _calculate_fifo_and_profit(self):
        for cur_str in self.get_currency_list():
            for i, row in self.get_dataframe_with_cond(cur=cur_str, buysell='SELL').iterrows():
                sold_crypto_amount = row['Määrä kryptovaluuttana']
                calculated_purchase_price_eur = self._update_jaljella_oleva_and_laske_ostohinta(sold_crypto_amount, cur_str)
                self.df.iloc[i]['Laskettu ostohinta'] = calculated_purchase_price_eur
                self.df.iloc[i]['Voitto'] = row['Hinta (EUR)'] - self.df.iloc[i]['Laskettu ostohinta']

    def _update_jaljella_oleva_and_laske_ostohinta(self, sold_crypto_amount: float, cur_str: str) -> float:
        calculated_purchase_price_eur = 0.0
        for i, row in self.get_dataframe_with_cond(cur=cur_str, buysell='BUY').iterrows():
            if sold_crypto_amount > 0:
                if row['Kryptovaluuttaa jäljellä (FIFO)'] != 0:  # TODO: tähän vois laittaa joku flägi, ettei tarvii joka myynnin yhteydessä iteroida jokaisen rivin läpi (jonka Kryptovaluuttaa jäljellä (FIFO) arvo on nolla)
                    if self.df.iloc[i]['Kryptovaluuttaa jäljellä (FIFO)'] >= sold_crypto_amount:
                        self.df.iloc[i]['Kryptovaluuttaa jäljellä (FIFO)'] = self.df.iloc[i]['Kryptovaluuttaa jäljellä (FIFO)'] - sold_crypto_amount
                        calculated_purchase_price_eur = calculated_purchase_price_eur + row['EUR/kryptovaluutta']*sold_crypto_amount
                        sold_crypto_amount = 0
                    elif sold_crypto_amount > self.df.iloc[i]['Kryptovaluuttaa jäljellä (FIFO)']:
                        sold_crypto_amount = sold_crypto_amount - self.df.iloc[i]['Kryptovaluuttaa jäljellä (FIFO)']
                        calculated_purchase_price_eur = calculated_purchase_price_eur + row['EUR/kryptovaluutta']*self.df.iloc[i]['Kryptovaluuttaa jäljellä (FIFO)']
                        self.df.iloc[i]['Kryptovaluuttaa jäljellä (FIFO)'] = 0

            else:
                break
        return calculated_purchase_price_eur

    def get_currency_list(self):
        df2 = self.df[['Kryptovaluutta', 'Hinta (EUR)']]
        df3 = df2.groupby(['Kryptovaluutta'], as_index='True')['Hinta (EUR)'].sum()
        df4 = df2.groupby(['Kryptovaluutta'], as_index='True')['Hinta (EUR)'].count()
        df5 = df4 * df3
        df5 = df5.sort_values(ascending=False)
        df5 = df5.index
        # currencylist = pd.Series(['BTC','ETH','CRO','DOGE','BNB','ICP','ADA','UNI','LTC','SHIB','XYO','DOT','TGBP','USDC'])
        return df5

    def get_year_list(self):
        df2 = self.df['Aikaleima']
        begin_year = df2.iloc[0].year
        end_year = df2.iloc[-1].year
        return list(range(begin_year, end_year+1))

    def get_yearly_profit_by_currency(self, year_str: int, cur_str: str):
        df = self.get_dataframe_with_cond(year=year_str, cur=cur_str, buysell='SELL')
        return df['Voitto'].sum()

    def get_net_invested_by_currency(self, cur_str: str):
        df_buy = self.get_dataframe_with_cond(cur=cur_str, buysell='BUY')
        df_sell = self.get_dataframe_with_cond(cur=cur_str, buysell='SELL')
        return df_buy['Hinta (EUR)'].sum() - df_sell['Hinta (EUR)'].sum()

    def get_dataframe_with_cond(self, cur: str=None, buysell: str=None, year: int=None):
        df = self.df
        if cur != None:
            df = df[df['Kryptovaluutta']==cur]
        if buysell != None:
            df = df[df['Osto/Myynti']==buysell]
        if year != None:
            cond = pd.DatetimeIndex(df['Aikaleima']).year == year
            df = df[cond] 
        return df


class RefinedDataWriter:

    def __init__(self, refined_data: RefinedData, outputfilename: str):
        assert type(refined_data) is RefinedData, "Input should be RefinedData"
        self.refined_data = refined_data
        self.outputfilename = outputfilename

    def run(self):
        cur_list = self.refined_data.get_currency_list()

        self.__add_first_line()
        for cur in cur_list:
            self.__add_currency_data_to_csv(cur)
            self.__add_yearly_profit_summary_by_currency(cur)
            self.__add_empty_lines_to_csv(1)
        self.__add_profit_summary_table()
        self.__add_empty_lines_to_csv(1)
        self.__add_portfolio_summary_table()

    def __add_first_line(self):
        df = self.refined_data.df.iloc[0:0]
        df.to_csv(self.outputfilename, mode='a', index=False)

    def __add_currency_data_to_csv(self, cur_str: str):
        df = self.refined_data.get_dataframe_with_cond(cur=cur_str)
        df.to_csv(self.outputfilename, mode='a', index=False, header=False)

    def __add_empty_lines_to_csv(self, empty_line_amount: int):
        df = pd.DataFrame()
        empty_strings = [''] * empty_line_amount
        series = pd.Series(empty_strings)
        df = pd.concat([df, series.to_frame()], ignore_index=True)
        df.to_csv(self.outputfilename, mode='a', index=False, header=False)

    def __add_yearly_profit_summary_by_currency(self, cur_str: str):
        df = pd.DataFrame()
        for year in self.refined_data.get_year_list():
            profit = self.refined_data.get_yearly_profit_by_currency(year, cur_str)
            row = [cur_str, 'Voitto vuodelta '+str(year), profit]
            series = pd.Series(row)
            df = pd.concat([df, series.to_frame().T], ignore_index=True)
        df.to_csv(self.outputfilename, mode='a', index=False, header=False)

    def __add_profit_summary_table(self):
        df = self.get_profit_summary_table()
        df.to_csv(self.outputfilename, mode='a')

    def get_profit_summary_table(self):
        year_list = self.refined_data.get_year_list()
        cur_list = list(self.refined_data.get_currency_list())
        df = pd.DataFrame(columns=year_list, index=cur_list)
        for i, row in df.iterrows():
            cur = row.name
            for year in year_list:
                profit = self.refined_data.get_yearly_profit_by_currency(year, cur)
                row[year] = profit
        return df

    def __add_portfolio_summary_table(self):
        df = self.get_portfolio_summary_table()
        df.to_csv(self.outputfilename, mode='a')
        
    def get_portfolio_summary_table(self):
        ind = ['Jäljellä (kryptovaluuttana)', 'Net invested']
        cur_list = list(self.refined_data.get_currency_list())
        df = pd.DataFrame(columns=ind, index=cur_list)
        for i, row in df.iterrows():
            cur_str = row.name
            df2 = self.refined_data.get_dataframe_with_cond(cur=cur_str)
            jaljella = df2['Kryptovaluuttaa jäljellä (FIFO)'].sum()
            row['Jäljellä (kryptovaluuttana)'] = jaljella
            net_invested = self.refined_data.get_net_invested_by_currency(cur_str)
            row['Net invested'] = net_invested
        return df

    
