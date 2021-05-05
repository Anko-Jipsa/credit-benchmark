#%%
import plotly.graph_objs as go
import plotly
from scripts import data_proc as dp
import numpy as np

DELOITTE_COLOURS = [
    "#2C5234", "#009A44", "#86BC25", "#C4D600", "#E3E48D", "#004F59",
    "#0097A9", "#6FC2B4", "#DDEFE8"
]


def canvas() -> plotly.graph_objects:
    """ Create plotly.graph_objects template with custom layout for macroeconomic variable.

    Args:
        macro_var (str): Macroeconomic variable.

    Returns:
        plotly.graph_objects: Empty canvas for a macroeconomic variable.
    """
    # Create Figure.
    custom_layout = go.Layout(template="plotly_white",
                              legend=dict(orientation="h"))
    fig = go.Figure(layout=custom_layout)
    fig.update_layout(hoverlabel_align='right',
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=1.02,
                                  xanchor="right",
                                  x=1),
                      xaxis=dict(showline=True,
                                 showgrid=False,
                                 showticklabels=True,
                                 linecolor='rgb(204, 204, 204)',
                                 linewidth=2,
                                 ticks='outside',
                                 tickfont=dict(
                                     family='Arial',
                                     size=12,
                                     color='rgb(82, 82, 82)',
                                 )))
    fig.update_xaxes(tickformat="%Y-Q%q")
    return fig


def add_portfolio_distribution(fig, pivoted_df):
    institutes = pivoted_df.index.get_level_values("Institute").unique()
    portfolios = pivoted_df.index.get_level_values("Portfolio").unique()

    for i, port in enumerate(portfolios):
        fig.add_trace(
            go.Bar(
                name=port,
                x=institutes,
                y=pivoted_df.xs(port, level="Portfolio").values.flatten(),
                hovertemplate='%{y:.2f}%',
                marker_color=DELOITTE_COLOURS[i],
            ))

    fig.update_layout(barmode='stack')
    return fig


def add_horizontal_bar(fig, pivoted_df, id):
    institutes = pivoted_df.index.get_level_values("Institute").unique()
    fig.add_trace(
        go.Bar(y=institutes,
               x=pivoted_df.values.flatten(),
               marker_color=DELOITTE_COLOURS[id],
               orientation='h',
               hovertemplate='%{x:.2f}%',
               texttemplate="%{x:.2f}%",
               textposition="inside",
               name=pivoted_df.columns[0]))
    return fig


def add_quarterly_bars(fig, pivoted_df):
    quarters = pivoted_df.index.get_level_values("Quarter").unique()
    institutes = pivoted_df.index.get_level_values("Institute").unique()

    for i, val in enumerate(institutes):
        fig.add_trace(
            go.Bar(
                name=val,
                x=quarters,
                y=pivoted_df.xs(val, level="Institute").values.flatten(),
                marker_color=DELOITTE_COLOURS[i],
                hovertemplate='%{y:.2f}%',
                texttemplate="%{y:.2f}%",
                textposition="inside",
            ))

    return fig


def add_portfolio_bar(fig, pivoted_df, portfolio):
    institutes = pivoted_df.index.get_level_values("Institute").unique()
    pivoted_df = dp.filter_portfolio_pivot(pivoted_df, portfolio)

    tot_avg = pivoted_df.groupby(level=[0, 2]).mean()
    tot_avg = dp.filter_portfolio_pivot(tot_avg, portfolio).values[0]
    fig.add_trace(
        go.Bar(
            name=portfolio,
            x=institutes,
            y=pivoted_df.values.flatten(),
            marker_color=DELOITTE_COLOURS[0],
            hovertemplate='%{y:.2f}%',
            texttemplate="%{y:.2f}%",
            textposition="inside",
        ))
    fig.add_trace(
        go.Scatter(
            name="Average",
            x=institutes,
            y=np.tile(tot_avg, (len(institutes), 1)).flatten(),
            hovertemplate='%{y:.2f}%',
            marker_color=DELOITTE_COLOURS[3],
        ))
    return fig


def avg_portfolio_distribution_time(fig, df, portfolio):
    portfolios = df.index.get_level_values("Portfolio").unique()
    quarters = df.index.get_level_values("Quarter").unique()

    fig.add_trace(
        go.Scatter(
            name="Average",
            x=quarters,
            y=df.xs(portfolio, level="Portfolio").values.flatten(),
            marker_color=DELOITTE_COLOURS[0],
            hovertemplate='%{y:.2f}%',
        ))
    return fig


def ind_portfolio_distribution_time(fig, df, portfolio):
    portfolios = df.index.get_level_values("Portfolio").unique()
    quarters = df.index.get_level_values("Quarter").unique()
    institutes = df.index.get_level_values("Institute").unique()

    for i, item in enumerate(institutes):
        _df = df[df.index.get_level_values("Institute") == item]
        fig.add_trace(
            go.Scatter(
                name=item,
                x=quarters,
                y=_df.xs(portfolio, level="Portfolio").values.flatten(),
                marker_color=DELOITTE_COLOURS[i + 1],
                hovertemplate='%{y:.2f}%',
            ))
    return fig