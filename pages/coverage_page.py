from scripts import data_proc as dp
from scripts import visual_func as vf
import streamlit_func as sf
import streamlit as st


def coverage_quarterly_bar_plot(df):
    fig = vf.canvas()
    fig = vf.add_quarterly_bars(fig, df)
    return fig


def main(df):
    st.title("Coverage Ratio Analysis")
    st.header("Filter")
    col1, col2 = st.beta_columns([2, 1])
    with col1:
        stage = sf.stage_selector(df, "Coverage Ratio", side_bar=False)
    with col2:
        portfolio = sf.portfolio_select(df, side_bar=False)

    st.write("---")
    df = dp.filter_portfolio(df, portfolio)
    df = dp.pivot_df(df, "Coverage Ratio", stage)

    st.header("Coverage")
    st.subheader("Quarter")
    st.write(coverage_quarterly_bar_plot(df))
