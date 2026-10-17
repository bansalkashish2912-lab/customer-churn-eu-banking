from pathlib import Path
import pandas as pd


def load_dataset(csv_path: str | Path) -> pd.DataFrame:
    """Load the churn dataset and validate required columns."""
    df = pd.read_csv(csv_path)

    required_columns = {
        "CustomerId",
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
        "Exited",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare the dataset for segmentation and churn analytics."""
    cleaned = df.copy()

    # Drop non-analytical field
    if "Surname" in cleaned.columns:
        cleaned = cleaned.drop(columns=["Surname"], errors="ignore")

    # Standardize binary fields
    binary_fields = ["HasCrCard", "IsActiveMember", "Exited"]
    for field in binary_fields:
        if field in cleaned.columns:
            cleaned[field] = cleaned[field].astype(int)

    # Keep essential categorical fields consistent
    for col in ["Geography", "Gender"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()

    return cleaned


def create_segmentation_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived segmentation columns for the churn analysis."""
    segmented = df.copy()

    # Age groups
    conditions = [
        segmented["Age"] < 30,
        (segmented["Age"] >= 30) & (segmented["Age"] < 46),
        (segmented["Age"] >= 46) & (segmented["Age"] <= 60),
        segmented["Age"] > 60,
    ]
    labels = ["<30", "30-45", "46-60", "60+"]
    segmented["AgeGroup"] = pd.cut(
        segmented["Age"],
        bins=[0, 29, 45, 60, float("inf")],
        labels=labels,
        right=False,
        include_lowest=True,
    )

    # Credit score bands
    if "CreditScore" in segmented.columns:
        segmented["CreditBand"] = pd.cut(
            segmented["CreditScore"],
            bins=[0, 500, 650, 800, float("inf")],
            labels=["Low", "Medium", "High", "Very High"],
            right=False,
            include_lowest=True,
        )

    # Tenure groups
    if "Tenure" in segmented.columns:
        segmented["TenureGroup"] = pd.cut(
            segmented["Tenure"],
            bins=[-1, 2, 5, float("inf")],
            labels=["New", "Mid-term", "Long-term"],
            right=False,
            include_lowest=True,
        )

    # Balance segments
    if "Balance" in segmented.columns:
        segmented["BalanceGroup"] = pd.cut(
            segmented["Balance"],
            bins=[-1, 0, 15000, float("inf")],
            labels=["Zero-balance", "Low-balance", "High-balance"],
            right=False,
            include_lowest=True,
        )

    return segmented


def build_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a high-level churn summary by segment."""
    summary = (
        df.groupby(["Geography", "AgeGroup", "TenureGroup"], dropna=False)["Exited"]
        .mean()
        .reset_index(name="ChurnRate")
    )
    return summary
