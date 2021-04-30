import streamlit as st
import streamlit_func as sf
from scripts import data_proc as dp
from pages import *

country = sf.country_select()
df = dp.read_file(country)
item = sf.item_selector()

if item == "Front":
    st.header("FRONT PAGE")

elif (item == "ECL") | (item == "EAD"):
    stage = sf.stage_selector(df, item)
    date = sf.quarter_selector(df)
    institutes = sf.institute_select(df)

    if institutes:
        df = dp.filter_institute(df, *institutes)
        df = dp.pivot_df(df, item, stage)
        ecl_ead_page.main(df, item, stage, date)

    else:
        st.warning("Please Select Institutes.")

elif item == "Coverage Ratio":
    stage = sf.stage_selector(df, item)
    portfolio = sf.portfolio_select(df)
    institutes = sf.institute_select(df)

    if institutes:
        df = dp.filter_institute(df, *institutes)
        df = dp.filter_portfolio(df, portfolio)
        df = dp.pivot_df(df, item, stage)
        coverage_page.main(df)

    else:
        st.warning("Please Select Institutes.")

elif item == "Staging balances (%)":
    stage = sf.stage_selector(df, item)
    portfolio = sf.portfolio_select(df)
    institutes = sf.institute_select(df)

    if institutes:
        df = dp.filter_institute(df, *institutes)
        df = dp.filter_portfolio(df, portfolio)
        df = dp.pivot_df(df, item, stage)
        stage_prop_page.main(df)

    else:
        st.warning("Please Select Institutes.")
