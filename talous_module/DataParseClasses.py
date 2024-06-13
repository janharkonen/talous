import pandas as pd

pd.set_option('display.max_columns', None)

class RawData:

    def __init__(self, filename : str) -> None:
        self.filename = filename
        self.df = pd.read_csv(filename)
