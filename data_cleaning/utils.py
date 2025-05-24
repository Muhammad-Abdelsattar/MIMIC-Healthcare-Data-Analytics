import pandas as pd


def convert_to_hive_timestamps(df, timestamp_cols):
    """Convert pandas datetime to PyArrow timestamps with millisecond precision"""
    for col in timestamp_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]).dt.floor("us")
    return df
