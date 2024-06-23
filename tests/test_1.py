from context import talous_module
from talous_module.helper_functions import *
from talous_module.DataParseClasses import *
from typing import cast

import unittest

TEST_INPUT_FILE = '../yksityinen/crypto_transactions_record_test.csv'

class TestDataTransformation(unittest.TestCase):
    def test_RawData(self):
        RawData1 = RawData(TEST_INPUT_FILE)
        self.assertEqual(RawData1.filename, TEST_INPUT_FILE)

        RawDataScraper1 = RawDataScraper(TEST_INPUT_FILE)

        list = ['BTC','CRO','ETH','USDC','DOT','BNB','DOGE','ADA','ICP','SHIB','TGBP','UNI','XYO','LTC']
        for i in range(0,len(list)):
            self.assertEqual(RawDataScraper1.get_currency_list()[i], list[i])

if __name__ == '__main__':
    unittest.main()