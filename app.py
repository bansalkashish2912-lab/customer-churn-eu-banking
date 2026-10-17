import streamlit as st

from src.data_utils import list_available_data_files
from src.churn_analysis import load_app_data, render_filters, render_kpis

st.set_page_config(page_title="Bank Churn Explorer", layout="wide")
st.title("Customer Segmentation & Churn Pattern Analytics in European Banking")

available_files = list_available_data_files()
selected_file = st.sidebar.selectbox("Select dataset", available_files or ["No dataset found"]) if available_files else "No dataset found"

if selected_file == "No dataset found":
    st.warning("Add a CSV dataset to the `data/` folder to begin analysis.")
    st.stop()

try:
    df = load_app_data(selected_file)
    filtered_df = render_filters(df)
    render_kpis(filtered_df)

    st.subheader("Churn by Geography")
    geography_summary = (
        filtered_df.groupby("Geography", dropna=False)["Exited"]
        .mean()
        .sort_values(ascending=False)
        .reset_index(name="ChurnRate")
    )
    st.bar_chart(geography_summary.set_index("Geography")["ChurnRate"] * 100)

    st.subheader("Segment Overview")
    segment_summary = (
        filtered_df.groupby(["Geography", "AgeGroup", "TenureGroup"], dropna=False)["Exited"]
        .mean()
        .reset_index(name="ChurnRate")
    )
    st.dataframe(segment_summary.sort_values("ChurnRate", ascending=False), use_container_width=True)

except Exception as exc:
    st.error(f"Unable to load dataset: {exc}")
