from helper_functions import *
from cryptocom_verolaskelmat import *
from DataParseClasses import *

#assert sum([1, 2, 3]) == 6, "Should be 6"
INPUT_FILE = 'D:/Python-projektit/yksityinen/crypto_transactions_record_test.csv'
OUTPUT_FILE = 'output_2024.csv'
pd.set_option('display.max_rows', None)
def main():

    RawData1 = CsvToRawData(INPUT_FILE)
    ARefinedData = RefinedData(RawData1.df)
    ARefinedData.df

if __name__ == '__main__':
    main()