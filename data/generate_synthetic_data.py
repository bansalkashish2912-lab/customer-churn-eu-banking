"""Generate a synthetic bank churn dataset for demo and testing.

Run:
    python data/generate_synthetic_data.py --output data/bank_churn.csv --n 2000
"""
import argparse
import random
import csv
from pathlib import Path

SURNAMES = [
    'Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
    'Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin'
]

GEOGRAPHIES = ['France', 'Spain', 'Germany']
GENDERS = ['Male', 'Female']


def generate_row(i: int):
    customer_id = 100000 + i
    surname = random.choice(SURNAMES)
    credit_score = int(random.gauss(650, 70))
    credit_score = max(300, min(900, credit_score))
    geography = random.choices(GEOGRAPHIES, weights=[0.4,0.3,0.3])[0]
    gender = random.choice(GENDERS)
    age = int(random.gauss(45, 12))
    age = max(18, min(90, age))
    tenure = int(max(0, min(10, random.expovariate(1/3))))
    # Many customers with zero balance
    if random.random() < 0.25:
        balance = 0.0
    else:
        balance = round(abs(random.gauss(40000, 60000)), 2)
    num_products = random.choices([1,2,3,4], weights=[0.6,0.3,0.08,0.02])[0]
    has_cr_card = random.choices([0,1], weights=[0.3,0.7])[0]
    is_active = random.choices([0,1], weights=[0.4,0.6])[0]
    estimated_salary = round(abs(random.gauss(60000, 25000)), 2)

    # Simple churn probability model for synthetic data
    churn_prob = 0.12
    if balance == 0:
        churn_prob += 0.08
    if is_active == 0:
        churn_prob += 0.10
    if age < 30:
        churn_prob += 0.05
    if tenure <= 1:
        churn_prob += 0.04
    if credit_score < 500:
        churn_prob += 0.03
    churn_prob = min(churn_prob, 0.8)
    exited = int(random.random() < churn_prob)

    return [customer_id, surname, credit_score, geography, gender, age, tenure, balance, num_products, has_cr_card, is_active, estimated_salary, exited]


def main(output: str, n: int):
    Path(output).resolve().parent.mkdir(parents=True, exist_ok=True)
    header = ['CustomerId','Surname','CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary','Exited']
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(n):
            writer.writerow(generate_row(i))
    print(f"Generated {n} rows to {output}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='data/bank_churn.csv')
    parser.add_argument('--n', type=int, default=1000)
    args = parser.parse_args()
    main(args.output, args.n)
