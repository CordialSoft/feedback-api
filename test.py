from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Write the alphabet to the first column
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i, letter in enumerate(alphabet, start=1):
    ws.cell(row=i, column=1, value=letter)

# Save the workbook to a file
wb.save("alphabet.xlsx")
