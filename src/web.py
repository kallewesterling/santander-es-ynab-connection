#!/usr/bin/env python3
"""
Flask web application for converting Santander Excel exports to YNAB CSV format.
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tempfile

from converter import convert_santander_to_ynab

app = Flask(__name__, template_folder='templates')
app.secret_key = 'santander-ynab-converter-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the upload form."""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """Handle file upload and conversion."""
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload an Excel file (.xls or .xlsx)', 'error')
        return redirect(url_for('index'))

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Convert to YNAB format
        transactions = convert_santander_to_ynab(input_path)

        # Save converted CSV
        output_filename = f"{os.path.splitext(filename)[0]}_ynab.csv"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        transactions.to_csv(output_path, index=False)

        # Clean up input file
        os.remove(input_path)

        # Send file to user
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='text/csv'
        )

    except Exception as e:
        flash(f'Error converting file: {str(e)}', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
