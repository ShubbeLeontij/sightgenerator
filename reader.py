import xlrd
import os
import generator

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "1.1"
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
    print("Reading", workbook.sheet_names()[sheet_num])

    for row_num in range(sheet.nrows):
        try:
            row = sheet.row_values(row_num)
            path = wt_path + row[0]
            convergence = int(row[1])
            speed = int(row[2])
            zoom = float(row[3])
            coord = list(map(float, row[4].split(',')))
            sight_type = row[5]

            generator.create_sight(path, speed, zoom, sight_type, coord, convergence)
        except ValueError:
            print('Wrong format string')

input("\nPress enter to exit")
