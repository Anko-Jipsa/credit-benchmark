import plotly.graph_objs as go
import plotly

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


def plot_distribution(fig, pivoed_df):
    institutes = pivoed_df.index.get_level_values("Institute").unique()
    portfolios = pivoed_df.index.get_level_values("Portfolio").unique()

    for i, port in enumerate(portfolios):
        fig.add_trace(
            go.Bar(
                name=port,
                x=institutes,
                y=pivoed_df.xs(port, level="Portfolio").values.flatten(),
                hovertemplate='%{y:.2f}%',
                marker_color=DELOITTE_COLOURS[i],
            ))

    fig.update_layout(barmode='stack')
    return fig


def add_horizontal_bar(fig, pivoed_df, id):
    institutes = pivoed_df.index.get_level_values("Institute").unique()
    fig.add_trace(
        go.Bar(y=institutes,
               x=pivoed_df.values.flatten(),
               marker_color=DELOITTE_COLOURS[id],
               orientation='h',
               hovertemplate='%{x:.2f}%',
               texttemplate="%{x:.2f}%",
               textposition="inside",
               name=pivoed_df.columns[0]))
    return fig


def pivoted_df_quarterly_bars(fig, pivoed_df):
    quarters = pivoed_df.index.get_level_values("Quarter").unique()
    institutes = pivoed_df.index.get_level_values("Institute").unique()

    for i, val in enumerate(institutes):
        fig.add_trace(
            go.Bar(
                name=val,
                x=quarters,
                y=pivoed_df.xs(val, level="Institute").values.flatten(),
                marker_color=DELOITTE_COLOURS[i],
                hovertemplate='%{y:.2f}%',
                texttemplate="%{y:.2f}%",
                textposition="inside",
            ))

    return fig