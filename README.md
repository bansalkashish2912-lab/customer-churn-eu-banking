# Customer Segmentation & Churn Pattern Analytics in European Banking

This repository contains a full analytics project focused on customer churn in European banking, including:

- Data validation and cleaning
- Segmentation analysis by geography, age, credit score, tenure, and balance
- Churn KPIs and profiling insights
- A Streamlit dashboard for interactive exploration
- Documentation and stakeholder-ready summaries

## Project goals

- Measure the overall churn rate
- Identify churn across customer segments
- Compare churn behavior across European countries
- Evaluate churn risk in high-value customer groups
- Support retention and customer strategy decisions

## Expected dataset

The project expects a CSV file with columns such as:

- CustomerId
- Surname
- CreditScore
- Geography
- Gender
- Age
- Tenure
- Balance
- NumOfProducts
- HasCrCard
- IsActiveMember
- EstimatedSalary
- Exited

Place the dataset in the `data/` folder, for example:

- `data/bank_churn.csv`

## Repository structure

```text
customer-churn-eu-banking/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── data/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── data_pipeline.py
│   └── churn_analysis.py
├── docs/
│   └── executive_summary.md
└── notebooks/
    └── exploratory_analysis.ipynb
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the dashboard

```bash
streamlit run app.py
```

## Run the analysis script

```bash
python src/churn_analysis.py
```

## Notes

- This project is designed to work with the standard churn dataset used in banking customer retention studies.
- The app dynamically filters by geography, gender, activity status, and age group.
- Dashboard KPIs can be expanded as additional business logic is added.

## Recommended next steps

1. Add the actual bank churn dataset to `data/`
2. Run the preprocessing pipeline
3. Validate churn segment distributions
4. Build final visuals and stakeholder narrative
5. Publish the dashboard and executive summary
