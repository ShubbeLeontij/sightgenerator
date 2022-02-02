import xlrd
import generator

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "0.0.2"
__email__ = "leontij03@yandex.ru"

sheet = xlrd.open_workbook('data.xlsx').sheet_by_index(0)
for row_num in range(1, sheet.nrows):
    row = sheet.row_values(row_num)
    foldername = row[0]
    filename = row[1]
    speed = int(row[2])
    zoom = float(row[3])
    sight_type = int(row[4])
    coord = list(map(float, row[5].split(',')))

    generator.create_sight(foldername, filename, speed, zoom, sight_type, coord)
