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
    fig = vf.add_portfolio_distribution(fig,
                                        distribution_table(df, stage, date))
    return fig


def portfolio_distribution_plot(df, stage, date, portfolio):
    fig = vf.canvas()
    fig = vf.add_portfolio_bar(fig, distribution_table(df, stage, date),
                               portfolio)
    return fig


def distribution_plot_time(df, stage, date, portfolio):
    _df = dp.distribution_pivot(df)
    fig = vf.canvas()
    fig = vf.avg_portfolio_distribution_time(
        fig,
        _df.groupby(["Quarter", "Portfolio"]).mean(), portfolio)
    fig = vf.ind_portfolio_distribution_time(fig, _df, portfolio)
    return fig


def quarterly_change_plot(df):
    fig = vf.canvas()
    fig = vf.add_horizontal_bar(fig, dp.diff_pivot_df(df, "2020Q2", "2019Q4"),
                                0)
    fig = vf.add_horizontal_bar(fig, dp.diff_pivot_df(df, "2020Q4", "2020Q2"),
                                2)
    return fig


def main(df, item):
    stage = sf.stage_selector(df, item)
    df = dp.pivot_df(df, item, stage)
    st.title(f"{item} Analysis")
    st.header("Filter(s)")
    st.write("---")

    st.header(f"{item} Distribution Analysis")
    date = st.selectbox(label="Select Date",
                        options=df.index.get_level_values("Quarter").unique())
    st.write(distribution_plot(df, stage, date))
    st.write("---")

    st.header(f"{item} Distribution Analysis by Portfolio")
    portfolio = st.selectbox(
        label="Select Portfolio",
        options=df.index.get_level_values("Portfolio").unique())
    st.write(portfolio_distribution_plot(df, stage, date, portfolio))
    st.write("---")

    st.header(f"{item} Distribution Analysis over Quarters")
    portfolio2 = st.selectbox(
        label="Select Portfolio",
        options=df.index.get_level_values("Portfolio").unique(),
        key="Sub2")
    st.write(distribution_plot_time(df, stage, date, portfolio2))
    st.write("---")

    st.header(f"{item} Quarterly Change Analysis")
    portfolio3 = st.selectbox(
        label="Select Portfolio",
        options=df.index.get_level_values("Portfolio").unique(),
        key="Sub3")
    _df = dp.filter_portfolio_pivot(df, portfolio3)
    st.write(quarterly_change_plot(_df))
    st.write("---")