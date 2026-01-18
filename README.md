# Santander to YNAB Converter

Convert Santander España credit card statements to YNAB-compatible CSV format.

Two options available:
- **CLI Script**: Simple command-line tool
- **Web Interface**: Browser-based converter (Dockerized)

---

## The Problem

Santander España credit card transaction statements can only be downloaded as Excel documents (.xls/.xlsx). YNAB does not support importing Excel files directly - it requires CSV format.

The real issue is that YNAB does not offer a live connection to Santander España credit card accounts, meaning transactions must be manually imported. Until YNAB provides native integration with Santander España, this converter serves as an intermediate solution to bridge the gap.

**What this tool does:**
- Converts Excel exports from Santander España to YNAB-compatible CSV
- Properly formats dates, amounts, and transaction details
- Enables manual import of credit card transactions into YNAB

---

## Option 1: CLI Script

### Usage

1. Export your Santander transactions to Excel (.xls or .xlsx)
2. Place the Excel file in the project folder
3. Run the script:

```bash
python3 src/cli.py
```

4. Import the generated `*_ynab.csv` file into YNAB

### Example

The `data/` folder contains sample files showing input and output:
- **Input**: `sample_santander_statement.xlsx` - Example Santander credit card statement
- **Output**: `sample_santander_statement_ynab.csv` - Converted file ready for YNAB import

The sample demonstrates how the converter transforms Spanish date formats (DD/MM/YYYY) to YNAB format (MM/DD/YYYY) and separates expenses and refunds into Outflow/Inflow columns.

---

## Option 2: Web Interface (Docker)

### Quick Start

Run the containerized web application:

```bash
# Using Docker
docker run -p 5000:5000 santander-ynab-converter

# Or using docker-compose
docker-compose up
```

Then open your browser to: **http://localhost:5000**

### Building from Source

```bash
# Build the Docker image
docker build -t santander-ynab-converter .

# Run the container
docker run -p 5000:5000 santander-ynab-converter
```

### Using the Web Interface

1. Open http://localhost:5000 in your browser
2. Click to select your Santander Excel file
3. Click "Convert to YNAB CSV"
4. Download the converted CSV file
5. Import into YNAB

---

## How It Works

- Finds transaction data in the Excel export
- Converts dates from DD/MM/YYYY to MM/DD/YYYY (YNAB format)
- Separates expenses and income into Outflow/Inflow columns
- Creates a clean CSV file ready for YNAB import

## CSV Format

The output CSV follows YNAB's standard format:
- **Date**: MM/DD/YYYY
- **Payee**: Merchant name
- **Memo**: Empty (fill in YNAB if needed)
- **Outflow**: Expenses (positive numbers)
- **Inflow**: Income (positive numbers)

---

## Contributing

Contributions are welcome! Whether you want to fix bugs, add features, or improve documentation, feel free to open an issue or submit a pull request.

### Getting Started

1. Fork the repository
2. Clone your fork locally
3. Install dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Test your changes with the sample data in `data/`
6. Submit a pull request

### Development

To run the web app locally for development:

```bash
python3 src/web.py
```

The application will be available at http://localhost:5000

### Project Structure

```
santander-ynab-connection/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── converter.py      # Shared conversion logic
│   ├── cli.py            # CLI conversion script
│   ├── web.py            # Flask web application
│   └── templates/
│       └── index.html    # Web interface template
├── data/                 # Sample data files
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
└── README.md
```

**Code Organization:**
- `src/converter.py` - Core conversion logic (reusable by both CLI and web)
- `src/cli.py` - Command-line interface
- `src/web.py` - Flask web application
- `src/templates/` - HTML templates for the web interface
- `data/` - Sample Santander statements for testing
