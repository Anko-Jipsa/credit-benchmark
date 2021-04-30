from scripts import data_proc as dp
from scripts import visual_func as vf
import streamlit_func as sf
import streamlit as st


def distribution_table(df, stage, date):
    df = dp.filter_quarter_pivot(df, start=date, end=date)
    df = dp.distribution_pivot(df)
    return df


def distribution_plot(df, stage, date):
    fig = vf.canvas()
    fig = vf.plot_distribution(fig, distribution_table(df, stage, date))
    return fig


def quarterly_change_plot(df):
    fig = vf.canvas()
    fig = vf.add_horizontal_bar(fig, dp.diff_pivot_df(df, "2020Q2", "2019Q4"),
                                0)
    fig = vf.add_horizontal_bar(fig, dp.diff_pivot_df(df, "2020Q4", "2020Q2"),
                                2)
    return fig


def main(df, item):
    st.header("Filter")
    stage = sf.stage_selector(df, item, side_bar=False)
    date = sf.quarter_selector(df, side_bar=False)
    institutes = sf.institute_select(df, side_bar=False)
    st.write("---")
    if institutes:
        df = dp.filter_institute(df, *institutes)
        df = dp.pivot_df(df, item, stage)

        st.header("ECL Distribution")
        st.subheader("Bank")
        st.write(distribution_plot(df, stage, date))

        st.header("ECL Quarterly Change")
        st.subheader("Bank")
        st.write(quarterly_change_plot(df))

    else:
        st.warning("Please Select Institutes.")