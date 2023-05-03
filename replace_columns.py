import openpyxl
from datetime import datetime

# Load the Excel file
wb = openpyxl.load_workbook('./results/ADO_extract.xlsx')
ws = wb.active

# Loop through the rows in the worksheet
for row in ws.iter_rows(min_row=2, values_only=False):
    planned_date = row[9]  # Column J is the 10th column (0-indexed)
    actual_date = row[10]  # Column K is the 11th column (0-indexed)
    actual_date_obj = None
    
    # Check if the actual date is in the future
    if actual_date.value is not None:
        actual_date_obj = datetime.strptime(actual_date.value, '%Y-%m-%dT%H:%M:%SZ')
        if actual_date_obj > datetime.now():
            # Replace the planned date with the actual date
            row[9].value = actual_date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
            row[10].value = None  # Delete the value in column K
            row[11].value = None  # Delete the value in column L
            
# Save the updated Excel file
wb.save('./results/ADO_extract.xlsx')
