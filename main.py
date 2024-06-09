import pandas as pd
from helper_functions import *
from cryptocom_verolaskelmat import *

INPUT_FILE = 'crypto_transactions_record_20240519_155200.csv'
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
def main():
    master_input_df = pd.read_csv(INPUT_FILE)

    master_output_df = run_verolaskelmat(master_input_df);

    outputfilename = 'output_2024.csv'
    master_output_df.to_csv(outputfilename, index=False)

if __name__ == '__main__':
    main()