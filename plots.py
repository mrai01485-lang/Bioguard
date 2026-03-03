import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def pest_risk_time_series(weather_df, risk_score):
    """
    Plot GDD and predicted pest risk over time
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=weather_df["date"],
        y=weather_df["GDD"],
        mode="lines",
        name="GDD"
    ))

    fig.add_trace(go.Scatter(
        x=weather_df["date"],
        y=[risk_score] * len(weather_df),
        mode="lines",
        name="Predicted Pest Risk",
        line=dict(dash="dash")
    ))

    fig.update_layout(
        title="Pest Risk Evolution Over Time",
        xaxis_title="Date",
        yaxis_title="Index"
    )

    return fig


def cost_effectiveness_plot(methods_df):
    """
    Scatter plot: Cost vs Effectiveness vs Risk
    """

    fig = px.scatter(
        methods_df,
        x="cost",
        y="effectiveness",
        size="risk",
        color="environmental_impact",
        hover_name="name",
        title="Cost vs Effectiveness vs Risk"
    )

    return fig


def risk_heatmap(methods_df):
    """
    Heatmap: Risk vs Effectiveness
    """

    fig = px.density_heatmap(
        methods_df,
        x="risk",
        y="effectiveness",
        title="Risk vs Effectiveness Heatmap"
    )

    return fig


def yield_gain_plot(methods_df):
    """
    Estimated yield gain by method
    """

    fig = px.bar(
        methods_df,
        x="name",
        y="estimated_yield_gain",
        title="Estimated Yield Gain by Method"
    )

    return fig
