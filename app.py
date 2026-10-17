import pandas as pd

from src.data_pipeline import build_churn_summary, clean_dataset, create_segmentation_features, load_dataset


def main():
    print("Loading churn dataset...")
    df = load_dataset("data/bank_churn.csv")
    df = clean_dataset(df)
    df = create_segmentation_features(df)

    summary = build_churn_summary(df)
    print("\nTop churn segments:")
    print(summary.sort_values("ChurnRate", ascending=False).head(10))

    total_churn_rate = df["Exited"].mean()
    print(f"\nOverall churn rate: {total_churn_rate:.2%}")


if __name__ == "__main__":
    main()
