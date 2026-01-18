#!/usr/bin/env python3
"""
CLI tool to convert Santander Excel export to YNAB-compatible CSV format.
"""

import sys
import os
import glob

from converter import convert_santander_to_ynab


def find_excel_file():
    """Find the Excel file in the current directory."""
    excel_files = glob.glob("*.xls") + glob.glob("*.xlsx")
    if not excel_files:
        print("Error: No Excel file found in the current directory.")
        sys.exit(1)
    if len(excel_files) > 1:
        print(f"Found multiple Excel files: {', '.join(excel_files)}")
        print(f"Using: {excel_files[0]}")
    return excel_files[0]


def main():
    """Main CLI entry point."""
    # Find and convert the Excel file
    input_file = find_excel_file()
    print(f"Converting: {input_file}")
    print("-" * 50)

    # Convert to YNAB format
    transactions = convert_santander_to_ynab(input_file)

    # Generate output filename
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_ynab.csv"

    # Save to CSV
    transactions.to_csv(output_file, index=False)

    print(f"✓ Converted {len(transactions)} transactions")
    print(f"✓ Saved to: {output_file}")
    print(f"\nYou can now import '{output_file}' into YNAB!")


if __name__ == "__main__":
    main()
