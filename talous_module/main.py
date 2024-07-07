from helper_functions import *
from cryptocom_verolaskelmat import *
from DataParseClasses import *

#assert sum([1, 2, 3]) == 6, "Should be 6"
INPUT_FILE = 'D:/Python-projektit/yksityinen/crypto_transactions_record_test_real_nums.csv'
OUTPUT_FILE = 'output_2024.csv'
pd.set_option('display.max_rows', None)
def main():

    raw_data = CsvToRawData(INPUT_FILE)
    refined_data = RefinedData(raw_data)
    writer = RefinedDataWriter(refined_data, OUTPUT_FILE)
    writer.run()

if __name__ == '__main__':
    main()