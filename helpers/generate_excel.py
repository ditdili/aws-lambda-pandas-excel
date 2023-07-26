import pandas as pd
import random
from datetime import datetime, timedelta

# Set random seed for repeatability
random.seed(42)


def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )


def generate_invoice_data(num_rows):
    start_date = datetime(2022, 12, 1)
    end_date = datetime(2023, 7, 31)

    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
    ]
    clothing_items = [
        "Shirt",
        "Pants",
        "Dress",
        "Shoes",
        "Socks",
        "Hat",
        "Scarf",
        "Jacket",
    ]

    data = []
    for _ in range(num_rows):
        invoice_date = random_date(start_date, end_date)
        invoice_amount = f"{random.randint(35, 1450)} USD"
        location_name = random.choice(cities)
        item_description = random.choice(clothing_items)

        data.append([invoice_date, invoice_amount, location_name, item_description])

    df = pd.DataFrame(
        data,
        columns=["Invoice Date", "Invoice Amount", "Location Name", "Item Description"],
    )

    # Sort the DataFrame by Invoice Date
    df = df.sort_values(by="Invoice Date").reset_index(drop=True)
    df["Invoice Date"] = df["Invoice Date"].dt.strftime("%m/%d/%Y")

    return df


# Save to Excel
with pd.ExcelWriter("mocks/invoices.xlsx", engine="openpyxl") as writer:
    # Empty Shipments sheet
    pd.DataFrame().to_excel(writer, sheet_name="Shipments", index=False)

    # Invoices sheet with data
    invoices_df = generate_invoice_data(1000)
    invoices_df.to_excel(writer, sheet_name="Invoices", index=False)

# Save to Excel
with pd.ExcelWriter("mocks/invoices_short.xlsx", engine="openpyxl") as writer:
    # Empty Shipments sheet
    pd.DataFrame().to_excel(writer, sheet_name="Shipments", index=False)

    # Invoices sheet with data
    invoices_df = generate_invoice_data(10)
    invoices_df.to_excel(writer, sheet_name="Invoices", index=False)
