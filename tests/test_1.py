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

    def test_RawDataScraper(self):
        RawDataScraper1 = RawDataScraper(TEST_INPUT_FILE)
        self.assertEqual(RawDataScraper1.filename, TEST_INPUT_FILE)

        RawData1 = CsvToRawDataFrame(TEST_INPUT_FILE)
        RawDataScraper2 = RawDataScraper(RawData1)
        self.assertEqual(RawDataScraper2.filename, TEST_INPUT_FILE)

        list = ['BTC','CRO','ETH','USDC','DOT','BNB','DOGE','ADA','ICP','SHIB','TGBP','UNI','XYO','LTC']
        for i in range(0,len(list)):
            self.assertTrue(RawDataScraper1._RawDataScraper__scrape_currency_list()[i] == list[i])

        self.assertEqual(RawDataScraper1._RawDataScraper__get_cur("EUR","ASD"), "ASD")
        self.assertEqual(RawDataScraper1._RawDataScraper__get_cur("QWE","EUR"), "QWE")
        self.assertEqual(RawDataScraper1._RawDataScraper__get_cur("QWE","ASD"), "NaN")

        list = [2021,2022,2023,2024]
        for i in range(0,len(list)):
            self.assertTrue(RawDataScraper1._RawDataScraper__scrape_year_list()[i] == list[i])

        

if __name__ == '__main__':
    unittest.main()