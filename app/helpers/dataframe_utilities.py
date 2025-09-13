"""
    Utilities and helpers for working with dataframes.
"""
import pandas as pd


def col_or_blank(df: pd.DataFrame, col: str, fill: str = '') -> pd.Series:
    """
    Return df[col] with NaNs filled with `fill` if the column exists,
    otherwise return a Series of `fill` with the same index as df.
    """
    if col in df.columns:
        return df[col].fillna(fill)
    return pd.Series(fill, index=df.index)


def safe_numeric_col(df: pd.DataFrame, col: str, dtype: str = "Float64") -> pd.Series:
    """
    Return df[col] with NaNs filled with `fill` if the column exists,
    """
    if col in df.columns:
        s = df[col]
    else:
        # Create aligned nullable float Series if the column is missing
        s = pd.Series(pd.NA, index=df.index, dtype=dtype)
    return pd.to_numeric(s, errors="coerce")
