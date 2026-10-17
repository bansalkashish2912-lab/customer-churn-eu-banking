import pandas as pd
import streamlit as st

from src.data_pipeline import clean_dataset, create_segmentation_features, load_dataset
from src.data_utils import get_data_path, list_available_data_files


@st.cache_data
def load_app_data(csv_file: str | None = None) -> pd.DataFrame:
    """Load and prepare the churn dataset for the Streamlit app."""
    if csv_file is None:
        files = list_available_data_files()
        if not files:
            raise FileNotFoundError("No CSV file found in data/. Add the dataset to the data folder.")
        csv_file = files[0]

    df = load_dataset(get_data_path(csv_file))
    df = clean_dataset(df)
    df = create_segmentation_features(df)
    return df


def render_filters(df: pd.DataFrame):
    """Render sidebar filters for the dashboard."""
    st.sidebar.header("Filters")
    geography = st.sidebar.multiselect("Geography", options=sorted(df["Geography"].dropna().unique().tolist()))
    gender = st.sidebar.multiselect("Gender", options=sorted(df["Gender"].dropna().unique().tolist()))
    age_group = st.sidebar.multiselect("Age Group", options=sorted(df["AgeGroup"].dropna().unique().tolist()))

    filtered = df.copy()
    if geography:
        filtered = filtered[filtered["Geography"].isin(geography)]
    if gender:
        filtered = filtered[filtered["Gender"].isin(gender)]
    if age_group:
        filtered = filtered[filtered["AgeGroup"].isin(age_group)]

    return filtered


def render_kpis(df: pd.DataFrame):
    """Render a KPI row with churn metrics."""
    total_customers = len(df)
    churn_rate = df["Exited"].mean() * 100 if total_customers else 0
    active_members = (df["IsActiveMember"] == 1).sum()
    avg_balance = df["Balance"].mean() if total_customers else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customers", f"{total_customers:,}")
    col2.metric("Churn Rate", f"{churn_rate:.2f}%")
    col3.metric("Active Members", f"{active_members:,}")
    col4.metric("Avg. Balance", f"€{avg_balance:,.0f}")
