import pandas as pd
import numpy as np
import re
import datetime
from pathlib import Path


def pre_process(df: pd.DataFrame) -> pd.DataFrame:
    """ This is pretty ugly data pre-processing code.
    This makes the dataset be inline with the German data.
    
    TODO: Refactor.

    Args:
        df (pd.DataFrame): UK Benchmark DataFrame.

    Returns:
        pd.DataFrame: Pre-processed darta.
    """
    df = df.iloc[2:].reset_index(drop=True)
    # Ffill na values
    df.iloc[0, :] = df.iloc[0, :].fillna(method="ffill")
    df = df.T  # Transpose

    # Merge item & attribute columns
    df['combined'] = df[[0, 1
                         ]].apply(lambda row: '_'.join(row.values.astype(str)),
                                  axis=1)
    df = df.iloc[2:, 2:]  # Drop redundant columns & rows
    df = df.T.iloc[::-1].reset_index(drop=True)  # Transpose & reverse
    df.columns = df.iloc[0, :]  # Promote headers
    df = df.iloc[1:]  # Drop promoted row

    # Remove loss-rate columns
    df = df[[col for col in df.columns if "Loss" not in col]]

    # Rename Asset columns to be in line with the other data
    df = column_rename(df, "Asset", "EAD")
    df = column_rename(df, "ECL", "ECL")
    df = column_rename(df, "Coverage", "Coverage Ratio")

    ead_cols = [col for col in df.columns if "EAD" in col]
    df[ead_cols] = df[ead_cols] * 1000  # Scale up (bn)
    cr_cols = [col for col in df.columns if "Coverage Ratio" in col]
    df[cr_cols] = df[cr_cols] * 100  # Percentage
    stage_cols = [col for col in df.columns if "Staging balances" in col]
    df[stage_cols] = df[stage_cols] * 100  # Percentage

    # Unpivot data
    df = pd.melt(df,
                 id_vars=df.columns[0:5],
                 var_name="Attr",
                 value_vars=df.columns[5:],
                 ignore_index=False)

    # Rename columns
    df = df.rename(
        {
            "Index_Client": "Institute",
            "Index_Date": "Quarter",
            "Index_Portfolio": "Portfolio",
            "Index_Currency": "FCCY",
            "Index_Conversion rate": "Exchange Rate"
        },
        axis=1)

    # Drop NaN rows
    df = df[~df["Attr"].str.contains("nan")]
    # Convert to float
    df.loc[:, "value"] = df.loc[:, "value"].astype(float)
    # Pivot data
    df = pd.pivot_table(
        df,
        values="value",
        index=["Institute", "Quarter", "Portfolio", "FCCY", "Exchange Rate"],
        columns="Attr").reset_index()
    # Rename columns for consistency
    df.columns = [column_name_parse(col) for col in df.columns]
    # Date convert
    df["Quarter"] = pd.PeriodIndex(df["Quarter"], freq="Q")

    # Remove redundant portfolios
    df = df.loc[df["Portfolio"].isin([
        "Mortgages", "Consumer Lending (including Auto Finance)",
        "Corporate & Commercial", "Other Loans & Advances", "Other Assets"
    ])]

    # Re-factoring no-needed (Too much effort)
    for item in ["EAD", "ECL"]:
        df[f"{item} Performing"] = df[f"{item} Stage 1"] + df[f"{item} Stage 2"]
        df[f"{item} Default"] = df[f"{item} Stage 3"] + df[f"{item} POCI"]

    df["NPL Ratio"] = df["EAD Performing"] / df["EAD Default"]

    for item in ["Performing", "Default"]:
        df[f"Coverage Ratio {item}"] = 100 * df[f"ECL {item}"] / df[
            f"EAD {item}"]

    for item in ["Stage 1", "Stage 2", "Stage 3"]:
        if item in ["Stage 1", "Stage 2"]:
            df[f"Share {item[0]}{item[-1]} (EAD)"] = 100 * df[
                f"EAD {item}"] / df["EAD Total"]
        else:
            df[f"Share {item[0]}{item[-1]}/Poci (EAD)"] = (
                100 * df[f"EAD {item}"] +
                df["EAD POCI"].fillna(0)) / df["EAD Total"]
    return df


def column_rename(df, old_str, new_sr):
    # Rename Asset columns to be in line with the other data
    original_cols = [col for col in df.columns if old_str in col]
    new_cols = [new_sr + "_" + col.split("_")[1] for col in original_cols]
    return df.rename(columns=dict(zip(original_cols, new_cols)))


def column_name_parse(col):
    if "_" in col:
        attr, item = col.split("_")
        reg_item = re.findall(r"S(.*)$", item)
        if reg_item:
            item = "Stage " + reg_item[0]
        col = attr + " " + item
    return col


if __name__ == "__main__":
    RAW_DB = Path.cwd() / "db/raw"
    PROCESSED_DB = Path.cwd() / "db/processed"
    df_map = pd.read_excel(RAW_DB / "uk_data.xlsx",
                           header=None,
                           sheet_name=None)
    sheets = [key for key in df_map.keys() if "Q" in key]

    dfs = pd.DataFrame()
    for sh in sheets:
        dfs = pd.concat([dfs, pre_process(df_map[sh])])

    dfs.to_csv(PROCESSED_DB / "uk_data_processed.csv")
