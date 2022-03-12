import openpyxl
import os
import generator

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "1.5"
__email__ = "leontij03@yandex.ru"


with open('path.txt', 'r') as f:
    wt_path = f.readline()
    if wt_path == '':
        wt_path = os.path.dirname(os.path.realpath(__file__)) + '\\output\\'
    else:
        wt_path += '\\UserSights\\'

workbook = openpyxl.load_workbook('data.xlsx')

for sheet_name in workbook.sheetnames:
    sheet = workbook[sheet_name]
    print("\nReading", sheet_name)

    for row_num in range(1, sheet.max_row + 1):
        path = None
        convergence = None
        speed = None
        zoom = None
        sight_type = None
        coord_x, coord_y = None, None
        try:
            path = wt_path + sheet.cell(row=row_num, column=1).value
            convergence = int(sheet.cell(row=row_num, column=2).value)
            speed = int(sheet.cell(row=row_num, column=3).value)
            zoom = float(sheet.cell(row=row_num, column=4).value)
            sight_type = sheet.cell(row=row_num, column=5).value

            coord_y, coord_x = tuple(map(float, sheet.cell(row=row_num, column=6).value.split(',')))
            for cell in sheet.cell(row=row_num, column=7).value, sheet.cell(row=row_num, column=8).value, sheet.cell(row=row_num, column=9).value:
                try:
                    coord_y, coord_x = coord_y + float(cell.split(',')[0]), coord_x + float(cell.split(',')[1])
                except ValueError:
                    pass
            for cell in sheet.cell(row=row_num, column=10).value, sheet.cell(row=row_num, column=11).value, sheet.cell(row=row_num, column=12).value:
                try:
                    coord_y, coord_x = coord_y - float(cell.split(',')[0]), coord_x - float(cell.split(',')[1])
                except ValueError:
                    pass
        except:
            pass
        try:
            generator.create_sight(path, speed, zoom, sight_type, [round(coord_y, 3), round(coord_x, 3)], convergence)
        except:
            print('Wrong format string')
input("\nPress enter to exit")
