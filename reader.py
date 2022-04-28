import os
import generator
try:
    import openpyxl
except:
    os.system('pip install openpyxl')
    import openpyxl

__author__ = "Shubbe Leontij"
__version__ = "2.0.2"


with open('path.txt', 'r') as f:
    wt_path = f.readline()
    if wt_path == '':
        wt_path = os.path.dirname(os.path.realpath(__file__)) + '/UserSights/'
    else:
        wt_path += '/UserSights/'
    try:
        os.mkdir(wt_path)
    except:
        pass

workbook = openpyxl.load_workbook('data.xlsx')

for sheet_name in workbook.sheetnames:
    sheet = workbook[sheet_name]
    print("\nReading", sheet_name)
    empty_rows = 0

    for row_excel in sheet.iter_rows(min_row=1, min_col=1, max_row=sheet.max_row, max_col=9):
        try:
            row = list(map(lambda cell: cell.value, row_excel))
            if row.count(None) == len(row):
                empty_rows += 1
                continue
            elif empty_rows:
                print(str(empty_rows) + ' empty rows')
                empty_rows = 0

            y, x = float(row[5].split(',')[0]), float(row[5].split(',')[1])
            if row[6] is not None:
                y, x = y + float(row[6].split(',')[0]), x + float(row[6].split(',')[1])
            if row[7] is not None:
                y, x = y - float(row[7].split(',')[0]), x - float(row[7].split(',')[1])
            if row[8] is not None:
                y, x = y - float(row[8].split(',')[0]), x - float(row[8].split(',')[1])

            generator.create_sight(wt_path + row[0], int(row[2]), float(row[3]), row[4], [round(y, 3), round(x, 3)], int(row[1]))
        except:
            print('Wrong string format')
    if empty_rows:
        print(str(empty_rows) + ' empty rows')

input("\nPress enter to exit")
