import streamlit as st
from scripts import data_proc as dp


def country_select(side_bar=True):
    # Setting up Segment and Item
    options = ["UK", "GERMANY"]
    if side_bar:
        return st.sidebar.selectbox(label="Select Country", options=options)
    else:
        return st.selectbox(label="Select Country", options=options)


def item_selector(side_bar=True):
    options = ["Front", "ECL", "EAD", "Coverage Ratio", "Staging balances (%)"]
    if side_bar:
        return st.sidebar.selectbox(label="Select Item", options=options)
    else:
        return st.selectbox(label="Select Item", options=options)


def stage_selector(df, item, side_bar=True):
    options = dp.search_stage_item(df, item)
    if side_bar:
        return st.sidebar.selectbox(label="Select Stage", options=options)
    else:
        return st.selectbox(label="Select Stage", options=options)


def quarter_selector(df, side_bar=True):
    if side_bar:
        return st.sidebar.selectbox(label="Select Quarter",
                                    options=df.Quarter.unique())
    else:
        return st.selectbox(label="Select Quarter",
                            options=df.Quarter.unique())


def institute_select(df, side_bar=True):
    if side_bar:
        return st.sidebar.multiselect(label="Select Institute",
                                      options=df.Institute.unique())
    else:
        return st.multiselect(label="Select Institute",
                              options=df.Institute.unique())


def portfolio_select(df, side_bar=True):
    if side_bar:
        return st.sidebar.selectbox(label="Select Portfolio",
                                    options=df.Portfolio.unique())
    else:
        return st.selectbox(label="Select Portfolio",
                            options=df.Portfolio.unique())