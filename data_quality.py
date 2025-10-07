import pandas as pd
import numpy as np

class DataQuality:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    # Summary Report
    def generate_report(self):
        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicate_count": self.df.duplicated().sum(),
            "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / (1024**2), 2),
        }

    # Missing Values
    def check_missing_values(self):
        return self.df[self.df.isnull().any(axis=1)]

    # Duplicates
    def check_duplicates(self):
        return self.df[self.df.duplicated()]

    # 4️⃣ Negative Amounts
    def check_negative_amounts(self, column="Amount"):
        if column in self.df.columns and pd.api.types.is_numeric_dtype(self.df[column]):
            return self.df[self.df[column] < 0]
        return pd.DataFrame()

    # 5️⃣ Invalid Dates
    def check_invalid_dates(self, column="Date"):
        if column in self.df.columns:
            invalid_mask = pd.to_datetime(self.df[column], errors="coerce").isna()
            return self.df[invalid_mask]
        return pd.DataFrame()

    # 6️⃣ Outliers (Z-Score)
    def check_outliers(self, column, threshold=3):
        if column in self.df.columns and pd.api.types.is_numeric_dtype(self.df[column]):
            z_scores = (self.df[column] - self.df[column].mean()) / self.df[column].std()
            return self.df[np.abs(z_scores) > threshold]
        return pd.DataFrame()

    # 7️⃣ Schema Validation
    def validate_schema(self, expected_schema: dict):
        """
        expected_schema = {
            "CustomerID": "int64",
            "Amount": "float64",
            "Date": "datetime64[ns]"
        }
        """
        schema_report = {}
        for col, dtype in expected_schema.items():
            if col not in self.df.columns:
                schema_report[col] = "❌ Missing Column"
            elif str(self.df[col].dtype) != dtype:
                schema_report[col] = f"⚠ Type Mismatch (Expected {dtype}, Found {self.df[col].dtype})"
            else:
                schema_report[col] = "✅ OK"
        return schema_report

    # 8️⃣ Correlation Matrix (for EDA)
    def correlation_matrix(self):
        numeric_df = self.df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            return numeric_df.corr()
        return pd.DataFrame()

