# Exploratory Analysis (Script)

This script performs exploratory data analysis for the bank churn dataset. Run it as a script or convert to a notebook for interactive use.

Usage:
    python notebooks/exploratory_analysis.py --input data/bank_churn.csv

Outputs:
- data/cleaned_bank_churn.csv (cleaned dataset)
- outputs/eda_summary.csv (segment churn rates)
- outputs/figures/*.png (visualizations)


import argparse
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.data_pipeline import load_dataset, clean_dataset, create_segmentation_features, build_churn_summary
from src.data_utils import get_data_path


def ensure_dirs():
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/figures").mkdir(exist_ok=True)


def main(input_path: str):
    ensure_dirs()
    csv = get_data_path(input_path) if not Path(input_path).exists() else Path(input_path)

    df = load_dataset(csv)
    df = clean_dataset(df)
    df = create_segmentation_features(df)

    # Save cleaned data
    df.to_csv("data/cleaned_bank_churn.csv", index=False)

    # Overall churn
    overall_churn = df["Exited"].mean()
    print(f"Overall churn rate: {overall_churn:.2%}")

    # Churn by geography
    geo = df.groupby("Geography")["Exited"].agg(["mean","count"]).reset_index().rename(columns={"mean":"churn_rate","count":"customers"})
    geo.to_csv("outputs/eda_churn_by_geography.csv", index=False)

    # Age group churn
    age = df.groupby("AgeGroup")["Exited"].agg(["mean","count"]).reset_index().rename(columns={"mean":"churn_rate","count":"customers"})
    age.to_csv("outputs/eda_churn_by_agegroup.csv", index=False)

    # Segment summary
    seg = build_churn_summary(df)
    seg.to_csv("outputs/eda_segment_summary.csv", index=False)

    # Simple visualizations
    plt.figure(figsize=(8,5))
    sns.barplot(data=geo, x="Geography", y="churn_rate")
    plt.title("Churn rate by Geography")
    plt.ylabel("Churn Rate")
    plt.savefig("outputs/figures/churn_by_geography.png", bbox_inches="tight")

    plt.figure(figsize=(8,5))
    sns.barplot(data=age, x="AgeGroup", y="churn_rate")
    plt.title("Churn rate by Age Group")
    plt.ylabel("Churn Rate")
    plt.savefig("outputs/figures/churn_by_agegroup.png", bbox_inches="tight")

    print("EDA artifacts saved to outputs/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='data/bank_churn.csv')
    args = parser.parse_args()
    main(args.input)
