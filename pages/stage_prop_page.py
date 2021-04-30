from scripts import data_proc as dp
from scripts import visual_func as vf
import streamlit_func as sf
import streamlit as st


def stage_proportion_bar_plot(df):
    fig = vf.canvas()
    fig = vf.pivoted_df_quarterly_bars(fig, df)
    return fig


def main(df):
    st.header("Filter")
    stage = sf.stage_selector(df, "Staging balances (%)", side_bar=False)
    portfolio = sf.portfolio_select(df, side_bar=False)
    institutes = sf.institute_select(df, side_bar=False)
    st.write("---")
    if institutes:
        df = dp.filter_institute(df, *institutes)
        df = dp.filter_portfolio(df, portfolio)
        df = dp.pivot_df(df, "Staging balances (%)", stage)

        st.header("Coverage")
        st.subheader("Quarter")
        st.write(stage_proportion_bar_plot(df))
