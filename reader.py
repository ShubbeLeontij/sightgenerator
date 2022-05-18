import os
import argparse
import generator
try:
    import openpyxl
except:
    try:
        os.system('pip install openpyxl')
        import openpyxl
    except:
        input('pip error\nPlease install pip and try again')
        exit()


__author__ = "Shubbe Leontij"
__version__ = "2.1"


def _print(string, severity=1):
    if MODE <= severity:
        print(string)


parser = argparse.ArgumentParser(description='Creates UserSights folder with WarThunder sights.')
parser.add_argument('-m', '--mode', help='Output mode. Development - 0 ; Normal - 1 (default); Silent - 2 ; Full silent - 3', default=1)
MODE = int(vars(parser.parse_args())['mode'])

with open('path.txt', 'r') as f:
    wt_path = f.readline()
    if wt_path == '':
        wt_path = os.path.dirname(os.path.realpath(__file__)) + '/UserSights/'
    else:
        wt_path += '/UserSights/'
    try:
        os.mkdir(wt_path)
        _print('Created folder %s' % wt_path, 0)
    except:
        pass
    _print('Writing in %s' % wt_path, 1)

wrong_strings = []
workbook = openpyxl.load_workbook('data.xlsx')

for sheet_name in workbook.sheetnames:
    sheet = workbook[sheet_name]
    _print("\nReading " + sheet_name, 1)
    wrong_strings.append(0)
    empty_rows = 0
    row_num = 0

    for row in sheet.iter_rows(min_row=1, min_col=1, max_row=sheet.max_row, max_col=9, values_only=True):
        row_num += 1
        _print(str(row), 0)
        try:
            if row.count(None) == len(row):
                empty_rows += 1
                continue
            elif empty_rows:
                _print(str(empty_rows) + ' empty rows', 0)
                empty_rows = 0

            y, x = float(row[5].split(',')[0]), float(row[5].split(',')[1])
            if row[6] is not None:
                y, x = y + float(row[6].split(',')[0]), x + float(row[6].split(',')[1])
            if row[7] is not None:
                y, x = y - float(row[7].split(',')[0]), x - float(row[7].split(',')[1])
            if row[8] is not None:
                y, x = y - float(row[8].split(',')[0]), x - float(row[8].split(',')[1])

            _print(generator.create_sight(wt_path + row[0], int(row[2]), float(row[3]), row[4], [round(y, 3), round(x, 3)], int(row[1])), 0)
        except:
            wrong_strings[-1] += 1
            _print('Wrong string format. Sheet: ' + sheet_name + ' Row: ' + row_num, 1)

    _print(str(empty_rows) + ' empty rows', 0)
    _print(str(wrong_strings[-1]) + ' errors', 1)

_print("\nExecution ended with " + str(sum(wrong_strings)) + " errors", 2)
if MODE <= 2:
    input("\nPress Enter to exit")
