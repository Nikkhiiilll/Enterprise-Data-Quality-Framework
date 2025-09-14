import pandas as pd
import numpy as np

class DataQuality:
    def __init__(self, df):
        self.df = df

    def check_missing_values(self):
        missing = self.df.isnull().sum()
        return missing[missing > 0]

    def check_duplicates(self):
        duplicates = self.df[self.df.duplicated()]
        return duplicates

    def check_negative_amounts(self):
        negatives = self.df[self.df['amount'] < 0]
        return negatives

    def check_invalid_dates(self):
        invalid_dates = self.df[~pd.to_datetime(self.df['date'], errors='coerce').notna()]
        return invalid_dates

    def generate_report(self):
        report = {
            "missing_values": self.check_missing_values().to_dict(),
            "duplicate_records": len(self.check_duplicates()),
            "negative_amounts": len(self.check_negative_amounts()),
            "invalid_dates": len(self.check_invalid_dates())
        }
        return report
