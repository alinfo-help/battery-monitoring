import os
import sys
import csv
from fpdf import FPDF

def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    try:
        with open('../data/battery_data.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for i, row in enumerate(csv_reader):
                if i == 0:
                    # Add the header row
                    header = ', '.join(row.keys())
                    pdf.cell(200, 10, txt=header, ln=True)
                # Add the data rows
                line = ', '.join(row.values())
                pdf.cell(200, 10, txt=line, ln=True)

        # Save the PDF to a file
        pdf_output_path = "battery_report.pdf"
        pdf.output(pdf_output_path)
        print(f"PDF report generated: {pdf_output_path}")

        # Open the PDF automatically
        if sys.platform == "win32":
            os.startfile(pdf_output_path)
        else:
            os.system(f"open {pdf_output_path}")
    except Exception as e:
        print(f"Error generating PDF report: {e}")
