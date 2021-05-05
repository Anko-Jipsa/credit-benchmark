from scripts import data_proc as dp
from scripts import visual_func as vf
import streamlit_func as sf
import streamlit as st


def stage_proportion_bar_plot(df):
    fig = vf.canvas()
    fig = vf.add_quarterly_bars(fig, df)
    return fig


def main(df):
    st.title(f"Stage Balance Analysis")
    st.header("Filter")
    portfolio = sf.portfolio_select(df, side_bar=False)
    stage = sf.stage_selector(df, "Staging balances (%)", side_bar=False)
    st.write("---")

    df = dp.filter_portfolio(df, portfolio)
    df = dp.pivot_df(df, "Staging balances (%)", stage)

    st.header(f"{stage} Balance Analysis")
    st.write(stage_proportion_bar_plot(df))
