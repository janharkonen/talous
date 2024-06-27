from context import talous_module
from talous_module.helper_functions import *
from talous_module.DataParseClasses import *
from typing import cast

import unittest

TEST_INPUT_CSV = 'D:/Python-projektit/yksityinen/crypto_transactions_record_test.csv'

class TestDataTransformation(unittest.TestCase):
    def test_RawData(self):
        RawData1 = CsvToRawDataFrame(TEST_INPUT_CSV)
        self.assertEqual(RawData1.filename, TEST_INPUT_CSV)

        with self.assertRaises(AssertionError) as context1:
            RawData1 = CsvToRawDataFrame('asd.notcsv')


    def test_RefinedData(self):
        with self.assertRaises(AssertionError) as context1:
            ARefinedData = RefinedData('asd')
        self.assertEqual('Input must be an instance of DataFrame', str(context1.exception))

        ARawData1 = CsvToRawDataFrame(TEST_INPUT_CSV)
        ARefinedData = RefinedData(ARawData1.df)

        #kelvolliset
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['crypto_earn_interest_paid'])
        self.assertEqual(tmpdf.shape[0], 192)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['referral_card_cashback'])
        self.assertEqual(tmpdf.shape[0], 1894)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['mco_stake_reward'])
        self.assertEqual(tmpdf.shape[0], 123)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['finance.lockup.dpos_compound_interest.crypto_wallet'])
        self.assertEqual(tmpdf.shape[0], 14)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['card_cashback_reverted'])
        self.assertEqual(tmpdf.shape[0], 25)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['viban_purchase'])
        self.assertEqual(tmpdf.shape[0], 72)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['crypto_viban_exchange'])
        self.assertEqual(tmpdf.shape[0], 48)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['crypto_purchase'])
        self.assertEqual(tmpdf.shape[0], 1)
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, [\
                                                                                    'crypto_earn_interest_paid', \
                                                                                    'referral_card_cashback', \
                                                                                    'mco_stake_reward', \
                                                                                    'finance.lockup.dpos_compound_interest.crypto_wallet', \
                                                                                    'card_cashback_reverted', \
                                                                                    'viban_purchase', \
                                                                                    'crypto_viban_exchange', \
                                                                                    'crypto_purchase'
                                                                                    ])
        self.assertEqual(tmpdf.shape[0], 2369)
        
        #kelvottomat
        tmpdf = ARefinedData._RefinedData__extract_relevant_lines_only(ARawData1.df, ['finance.dpos.compound_interest.crypto_wallet',
                                                                                        'crypto_earn_program_created',
                                                                                        'reward.loyalty_program.trading_rebate.crypto_wallet',
                                                                                        'finance.crypto_earn.loyalty_program_extra_interest_paid.crypto_wallet',
                                                                                        'crypto_earn_program_withdrawn',
                                                                                        'finance.dpos.staking.crypto_wallet',
                                                                                        'finance.lockup.dpos_lock.crypto_wallet',
                                                                                        'lockup_unlock',
                                                                                        'admin_wallet_credited',
                                                                                        'lockup_lock',
                                                                                        'crypto_transfer',
                                                                                        'referral_bonus',
                                                                                        'lockup_upgrade',
                                                                                        'card_top_up',
                                                                                        'referral_gift'])
        self.assertEqual(tmpdf.shape[0], 124)

        #self.assertTrue(ARefinedData._RefinedData__is_crypto_transaction('BTC -> EUR'))
        #self.assertTrue(ARefinedData._RefinedData__is_crypto_transaction('DOGE -> EUR'))
        #self.assertTrue(ARefinedData._RefinedData__is_crypto_transaction('EUR -> DOGE'))

        

if __name__ == '__main__':
    unittest.main()