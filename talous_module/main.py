import pandas as pd
from helper_functions import *
from cryptocom_verolaskelmat import *

#print(__name__)
#assert sum([1, 2, 3]) == 6, "Should be 6"
INPUT_FILE = '../yksityinen/crypto_transactions_record_20240519_155200.csv'
OUTPUT_FILE = 'output_2024.csv'
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
def main():
    master_input_df = pd.read_csv(INPUT_FILE)

    master_output_df = run_verolaskelmat(master_input_df);

    master_output_df.to_csv(OUTPUT_FILE, index=False)

if __name__ == '__main__':
    main()