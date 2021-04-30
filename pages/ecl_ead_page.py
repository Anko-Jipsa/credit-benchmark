from scripts import data_proc as dp
from scripts import visual_func as vf
import streamlit as st


def ecl_distribution_table(df, page, stage, date):
    df = dp.filter_quarter_pivot(df, start=date, end=date)
    df = dp.distribution_pivot(df)
    return df


def ecl_distribution_plot(df, page, stage, date):
    fig = vf.canvas()
    fig = vf.plot_distribution(fig,
                               ecl_distribution_table(df, page, stage, date))
    return fig


def ecl_quarterly_change_plot(df):
    fig = vf.canvas()
    fig = vf.add_horizontal_bar(fig, dp.diff_pivot_df(df, "2020Q2", "2019Q4"))
    fig = vf.add_horizontal_bar(fig, dp.diff_pivot_df(df, "2020Q4", "2020Q2"))
    return fig


def main(df, page, stage, date):
    st.header("ECL Distribution")
    st.subheader("Bank")
    st.write(ecl_distribution_plot(df, page, stage, date))

    st.header("ECL Quarterly Change")
    st.subheader("Bank")
    st.write(ecl_quarterly_change_plot(df))