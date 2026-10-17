# Dashboard components

This module contains helper functions for KPI calculations and Plotly visualizations used by the Streamlit app.

import pandas as pd
import plotly.express as px


def compute_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    churn_rate = df['Exited'].mean() if total else 0
    high_value_churn = df[df['Balance'] > df['Balance'].median()]['Exited'].mean() if total else 0
    avg_balance = df['Balance'].mean() if total else 0
    return {
        'total_customers': total,
        'churn_rate': churn_rate,
        'high_value_churn': high_value_churn,
        'avg_balance': avg_balance,
    }


def plot_churn_by_geo(df: pd.DataFrame):
    geo = df.groupby('Geography')['Exited'].mean().reset_index(name='churn_rate')
    fig = px.bar(geo, x='Geography', y='churn_rate', title='Churn Rate by Geography', labels={'churn_rate':'Churn Rate'})
    return fig


def plot_churn_by_agegroup(df: pd.DataFrame):
    age = df.groupby('AgeGroup')['Exited'].mean().reset_index(name='churn_rate')
    fig = px.bar(age, x='AgeGroup', y='churn_rate', title='Churn Rate by Age Group', labels={'churn_rate':'Churn Rate'})
    return fig
