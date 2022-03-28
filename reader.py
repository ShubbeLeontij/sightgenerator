import openpyxl
import os
import generator

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "1.7"
__email__ = "leontij03@yandex.ru"


with open('path.txt', 'r') as f:
    wt_path = f.readline()
    if wt_path == '':
        wt_path = os.path.dirname(os.path.realpath(__file__)) + '/output/'
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

    for row in sheet.iter_rows(min_row=1, min_col=1, max_row=sheet.max_row, max_col=12):
        empty = True
        for cell in row:
            if cell.value is not None:
                empty = False
        if empty:
            continue

        coord_y, coord_x = None, None
        try:
            coord_y, coord_x = float(row[5].value.split(',')[0]), float(row[5].value.split(',')[1])
        except:
            pass
        for cell in row[6].value, row[7].value, row[8].value:
            try:
                coord_y, coord_x = coord_y + float(cell.split(',')[0]), coord_x + float(cell.split(',')[1])
            except:
                pass
        for cell in row[9].value, row[10].value, row[11].value:
            try:
                coord_y, coord_x = coord_y - float(cell.split(',')[0]), coord_x - float(cell.split(',')[1])
            except:
                pass

        generator.create_sight(wt_path + row[0].value, int(row[2].value), float(row[3].value), row[4].value, [round(coord_y, 3), round(coord_x, 3)], int(row[1].value))


input("\nPress enter to exit")
