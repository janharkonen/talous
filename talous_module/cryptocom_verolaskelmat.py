import pandas as pd
from pandas import DataFrame
from helper_functions import *
#print(__name__)
def run_verolaskelmat(input_df : DataFrame) -> DataFrame:
    output_df = create_empty_output_DataFrame()

    currencylist = get_currency_list(input_df)
    #print(currencylist)
    #print(input_df.info())
    yearlist = get_year_list(input_df)
    #print(yearlist)

    cur = currencylist[0]
    cur_df = parse_currency(input_df, cur)




    #for currency in currencylist:

    #print(input_df.info())

    return output_df