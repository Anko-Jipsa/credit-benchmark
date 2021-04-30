from scripts import data_proc as dp
from scripts import visual_func as vf
import streamlit as st


def coverage_quarterly_bar_plot(df):
    fig = vf.canvas()
    fig = vf.pivoted_df_quarterly_bars(fig, df)
    return fig


def main(df):
    st.header("Coverage")
    st.subheader("Quarter")
    st.write(coverage_quarterly_bar_plot(df))
