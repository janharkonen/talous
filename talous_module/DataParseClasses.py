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


class RefinedDataByCurrency:

    def __init__(self, df_in: DataFrame, cur: str):
        self.currency = cur
        self.df = df_in
        self.df_buy = self.get_dataframe_by_buysell('BUY')
        self.df_sell = self.get_dataframe_by_buysell('SELL')
        self.calculate_fifo_and_profit()
        self.df = pd.concat([self.df_buy, self.df_sell], ignore_index=True)
        self.df = self.df.sort_values(by=['Aikaleima'])

    def calculate_fifo_and_profit(self) -> None:
        for i, row in self.df_sell.iterrows():
            sold_crypto_amount = row['Määrä kryptovaluuttana']
            calculated_purchase_price_eur = self._update_jaljella_oleva_and_laske_ostohinta(sold_crypto_amount)
            row['Laskettu ostohinta'] = calculated_purchase_price_eur
            row['Voitto'] = row['Hinta (EUR)'] - row['Laskettu ostohinta']

    def _update_jaljella_oleva_and_laske_ostohinta(self, sold_crypto_amount: float) -> float:
        calculated_purchase_price_eur = 0.0
        for i, row in self.df_buy.iterrows():
            if sold_crypto_amount > 0:
                if row['Kryptovaluuttaa jäljellä (FIFO)'] != 0:  # TODO: tähän vois laittaa joku flägi, ettei tarvii joka myynnin yhteydessä iteroida jokaisen rivin läpi (jonka Kryptovaluuttaa jäljellä (FIFO) arvo on nolla)
                    if row['Kryptovaluuttaa jäljellä (FIFO)'] >= sold_crypto_amount:
                        row['Kryptovaluuttaa jäljellä (FIFO)'] = row['Kryptovaluuttaa jäljellä (FIFO)'] - sold_crypto_amount
                        calculated_purchase_price_eur = calculated_purchase_price_eur + row['EUR/kryptovaluutta']*sold_crypto_amount
                        sold_crypto_amount = 0
                    elif sold_crypto_amount > row['Kryptovaluuttaa jäljellä (FIFO)']:
                        sold_crypto_amount = sold_crypto_amount - row['Kryptovaluuttaa jäljellä (FIFO)']
                        calculated_purchase_price_eur = calculated_purchase_price_eur + row['EUR/kryptovaluutta']*row['Kryptovaluuttaa jäljellä (FIFO)']
                        row['Kryptovaluuttaa jäljellä (FIFO)'] = 0

            else:
                break
        return calculated_purchase_price_eur

    def get_dataframe_by_buysell(self, buysell: str) -> DataFrame:
        return self.df[self.df['Osto/Myynti'] == buysell]

    def get_yearly_profit(self, year: int) -> float:
        cond = pd.DatetimeIndex(self.df_sell['Aikaleima']).year == year
        df_year = self.df_sell[cond]
        return df_year['Voitto'].sum()

    def get_summary_data_frame(self, yearlist) -> DataFrame:
        return pd.DataFrame()


class RefinedData:

    def __init__(self, input: CsvToRawData) -> None:
        assert isinstance(input, CsvToRawData), "Input must be an instance of CsvToRawData"
        self.df = self.__convert_rawdata_to_refined(input.df)
        self.currency_list = self.__init_currency_list()
        self.year_list = self.__init_year_list()
        self.refined_data_by_currency_list = self.__create_refined_data_by_currency_list()

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

    def __create_refined_data_by_currency_list(self) -> list:
        lst = []
        for cur in self.get_currency_list():
            refined_data_by_currency = RefinedDataByCurrency(self.df[self.df['Kryptovaluutta'] == cur], cur)
            lst.append(refined_data_by_currency)
        return lst

    def __init_currency_list(self):
        df2 = self.df[['Kryptovaluutta', 'Hinta (EUR)']]
        df3 = df2.groupby(['Kryptovaluutta'], as_index='True')['Hinta (EUR)'].sum()
        df4 = df2.groupby(['Kryptovaluutta'], as_index='True')['Hinta (EUR)'].count()
        df5 = df4 * df3
        df5 = df5.sort_values(ascending=False)
        df5 = df5.index
        # currencylist = pd.Series(['BTC','ETH','CRO','DOGE','BNB','ICP','ADA','UNI','LTC','SHIB','XYO','DOT','TGBP','USDC'])
        return df5

    def __init_year_list(self):
        df2 = self.df['Aikaleima']
        begin_year = df2.iloc[0].year
        end_year = df2.iloc[-1].year
        return list(range(begin_year, end_year+1))

    def get_currency_list(self):
        return self.currency_list

    def get_year_list(self):
        return self.year_list

    def get_refined_data_by_currency(self, cur: str) -> DataFrame:
        return self.refined_data_by_currency_list[self.currency_list.get_loc(cur)]

    def get_yearly_profit_by_currency(self, year: int, cur: str):
        rd = self.get_refined_data_by_currency(cur)
        return rd.get_yearly_profit(year)
