import xlrd
import os
import generator

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "1.4"
__email__ = "leontij03@yandex.ru"


with open('path.txt', 'r') as f:
    wt_path = f.readline()
    if wt_path == '':
        wt_path = os.path.dirname(os.path.realpath(__file__)) + '\\output\\'
    else:
        wt_path += '\\UserSights\\'

workbook = xlrd.open_workbook('data.xlsx')

for sheet_num in range(workbook.nsheets):
    sheet = workbook.sheet_by_index(sheet_num)
    print("\nReading", workbook.sheet_names()[sheet_num])

    for row_num in range(sheet.nrows):
        try:
            row = sheet.row_values(row_num)
            path = wt_path + row[0]
            convergence = int(row[1])
            speed = int(row[2])
            zoom = float(row[3])
            sight_type = row[4]

            coord_y, coord_x = tuple(map(float, row[5].split(',')))
            for cell in row[6], row[7], row[8]:
                try:
                    coord_y, coord_x = coord_y + float(cell.split(',')[0]), coord_x + float(cell.split(',')[1])
                except ValueError:
                    pass
            for cell in row[9], row[10], row[11]:
                try:
                    coord_y, coord_x = coord_y - float(cell.split(',')[0]), coord_x - float(cell.split(',')[1])
                except ValueError:
                    pass

            generator.create_sight(path, speed, zoom, sight_type, [round(coord_y, 3), round(coord_x, 3)], convergence)
        except ValueError:
            print('Wrong format string')

input("\nPress enter to exit")
