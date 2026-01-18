#!/usr/bin/env python3
"""
Shared conversion logic for converting Santander Excel exports to YNAB CSV format.

YNAB CSV Format:
- Date (MM/DD/YYYY)
- Payee
- Memo (optional)
- Outflow (expenses as positive numbers)
- Inflow (income as positive numbers)
"""

import pandas as pd
from datetime import datetime


def convert_date_to_ynab_format(date_str):
    """Convert date from DD/MM/YYYY to MM/DD/YYYY format."""
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%m/%d/%Y")
    except ValueError:
        return date_str


def convert_santander_to_ynab(input_file):
    """
    Convert Santander Excel export to YNAB CSV format.

    Args:
        input_file: Path to the Santander Excel file

    Returns:
        pandas.DataFrame: Converted transactions in YNAB format
    """
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Extract transactions starting from row 7
    transactions = df.iloc[7:].copy()

    # Rename columns
    transactions.columns = ['Date', 'Payee', 'Amount']

    # Remove rows where Date is NaN
    transactions = transactions[transactions['Date'].notna()]

    # Convert dates to YNAB format
    transactions['Date'] = transactions['Date'].astype(str).apply(convert_date_to_ynab_format)

    # Clean up payee names
    transactions['Payee'] = transactions['Payee'].astype(str).str.strip()

    # Convert amount to float
    transactions['Amount'] = pd.to_numeric(transactions['Amount'], errors='coerce')

    # Add empty Memo column
    transactions['Memo'] = ''

    # Split Amount into Outflow and Inflow columns
    transactions['Outflow'] = transactions['Amount'].apply(lambda x: abs(x) if x < 0 else '')
    transactions['Inflow'] = transactions['Amount'].apply(lambda x: x if x > 0 else '')

    # Reorder columns
    transactions = transactions[['Date', 'Payee', 'Memo', 'Outflow', 'Inflow']]

    return transactions
