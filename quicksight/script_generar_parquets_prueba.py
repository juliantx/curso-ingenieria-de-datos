import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

np.random.seed(42)

# -----------------------
# Dataset 1: Customers
# -----------------------
n_customers = 50

customers = pd.DataFrame({
    "customer_id": range(1, n_customers + 1),
    "customer_name": [fake.name() for _ in range(n_customers)],
    "age": np.random.randint(18, 65, n_customers),
    "gender": np.random.choice(["Male", "Female"], n_customers),
    "signup_date": pd.date_range(start="2022-01-01", periods=n_customers, freq="7D"),
    "segment": np.random.choice(["Regular", "Premium", "VIP"], n_customers, p=[0.6, 0.3, 0.1]),
    "income_level": np.random.choice(["Low", "Medium", "High"], n_customers),
    "region": np.random.choice(["North", "South", "East", "West"], n_customers)
})

# -----------------------
# Dataset 2: Sales
# -----------------------
n_sales = 100

products = [
    ("Electronics", "Laptop"),
    ("Electronics", "Phone"),
    ("Clothing", "Shirt"),
    ("Clothing", "Shoes"),
    ("Home", "Chair"),
    ("Home", "Table")
]

sales_data = []

for i in range(1, n_sales + 1):
    category, product = random.choice(products)
    price = round(np.random.uniform(10, 1000), 2)
    quantity = np.random.randint(1, 5)
    discount = round(np.random.choice([0, 0.05, 0.1, 0.2]), 2)
    total = round(price * quantity * (1 - discount), 2)

    sales_data.append({
        "order_id": i,
        "date": fake.date_between(start_date="-1y", end_date="today"),
        "customer_id": np.random.randint(1, n_customers + 1),
        "city": fake.city(),
        "country": "Colombia",
        "product_category": category,
        "product_name": product,
        "price": price,
        "quantity": quantity,
        "discount": discount,
        "total_amount": total,
        "payment_method": random.choice(["Credit Card", "Debit Card", "Cash", "PSE"])
    })

sales = pd.DataFrame(sales_data)

customers.to_csv('customers.csv', index=False)
sales.to_csv('sales.csv', index=False)

# -----------------------
# Guardar en Parquet
# -----------------------
customers.to_parquet("customers.parquet", index=False)
sales.to_parquet("sales.parquet", index=False)

print("Archivos generados: customers.parquet y sales.parquet")
