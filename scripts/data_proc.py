import pandas as pd
from pathlib import Path


def read_file(country):
    folder_path = Path.cwd() / "db/processed"
    file_path = folder_path.resolve() / f"{country.lower()}_data_processed.csv"
    return pd.read_csv(file_path, index_col=0)


def pivot_df(df, item, stage):
    index_cols = ["Quarter", "Institute", "Portfolio"]
    return df.groupby(index_cols).agg({f"{item} {stage}": "sum"})


def diff_pivot_df(pivoted_df, date1, date2):
    pivoted_df = 100 * (
        pivoted_df.xs(date1, level=0) / pivoted_df.xs(date2, level=0) - 1)
    pivoted_df.columns = [f"{date1}-{date2}"]
    return pivoted_df


def distribution_pivot(pivoted_df):
    return pivoted_df.groupby(
        level=[0, 1]).apply(lambda x: 100 * x / float(x.sum()))


def filter_item_stage(df, item, stage):
    return df[[f"{item} {stage}"]]


def filter_quarter(df, start=None, end=None):
    if not end:
        end = max(df["Quarter"])
    if not start:
        start = min(df["Quarter"])
    return df.loc[(df["Quarter"] >= start) & (df["Quarter"] <= end)]


def filter_quarter_pivot(df, start=None, end=None):
    idx = pd.IndexSlice
    if not end:
        end = max(x.index.get_level_values(0))
    if not start:
        start = min(x.index.get_level_values(0))
    # return df.loc[idx[start:end, :, :], :]
    return df.query(f"(Quarter >= '{start}') & (Quarter <= '{end}')")


def filter_institute(df, *institutes):
    return df[df["Institute"].isin(institutes)]


def filter_institute_pivot(df, *institutes):
    return df[df.index.get_level_values("Institute").isin(institutes)]


def filter_portfolio(df, *portfolios):
    return df[df["Portfolio"].isin(portfolios)]


def filter_portfolio_pivot(df, *portfolios):
    return df[df.index.get_level_values("Portfolio").isin(portfolios)]


def search_stage_item(df, item):
    return [
        col.split(f"{item} ")[1] for col in df.columns
        if (item in col) & ("Share" not in col)
    ]
