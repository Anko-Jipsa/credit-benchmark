import streamlit as st
from scripts import data_proc as dp


def country_select():
    # Setting up Segment and Item
    options = ["UK", "GERMANY"]
    item = st.sidebar.selectbox(label="Select Country", options=options)
    return item


def item_selector():
    options = ["Front", "ECL", "EAD", "Coverage Ratio", "Staging balances (%)"]
    item = st.sidebar.selectbox(label="Select Item", options=options)
    return item


def stage_selector(df, item):
    options = dp.search_stage_item(df, item)
    item = st.sidebar.selectbox(label="Select Stage", options=options)
    return item


def quarter_selector(df):
    item = st.sidebar.selectbox(label="Select Quarter",
                                options=df.Quarter.unique())
    return item


def institute_select(df):
    item = st.sidebar.multiselect(label="Select Institute",
                                  options=df.Institute.unique())
    return item


def portfolio_select(df):
    item = st.sidebar.selectbox(label="Select Portfolio",
                                options=df.Portfolio.unique())
    return item