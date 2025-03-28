from weasyprint import HTML
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Input and output file paths
html_file = os.path.join(current_dir, 'ai_hedge_fund_report.html')
pdf_file = os.path.join(current_dir, 'ai_hedge_fund_report.pdf')

# Convert HTML to PDF
HTML(html_file).write_pdf(pdf_file)

print(f"PDF successfully created at: {pdf_file}")
