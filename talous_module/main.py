from helper_functions import *
from cryptocom_verolaskelmat import *
from DataParseClasses import *

#print(__name__)
#assert sum([1, 2, 3]) == 6, "Should be 6"
INPUT_FILE = 'D:/Python-projektit/yksityinen/crypto_transactions_record_20240519_155200.csv'
OUTPUT_FILE = 'output_2024.csv'
pd.set_option('display.max_rows', None)
def main():

    RawData1 = CsvToRawDataFrame(INPUT_FILE)
    ARefinedData = RefinedData(RawData1.df)

if __name__ == '__main__':
    main()