import xlrd
import xlwt
import random

def write03Excel(path):
    path1 = 'instructor1.xls'
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("instructor")

    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(sheets[0])
    lastc = ''
    lasts = ''
    m = 1
    for i in range(0, worksheet.nrows):
        if worksheet.cell_value(i, 0) == lastc:
            print(lastc)
            continue
        else:
            lastc = worksheet.cell_value(i, 0)
        for j in range(0, worksheet.ncols):
            value = worksheet.cell_value(i, j)
            # if j==4 and int(value) == 0:
            #     if random.randint(0,9) > 6:
            #         sheet.write(m, 7, 1)
            #     else:
            #         sheet.write(m, 7, 0)
            sheet.write(m, j, value)
        m += 1
    wb.save(path1)


def read03Excel(path):
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(sheets[0])
    for i in range(0, worksheet.nrows):
        row = worksheet.row(i)
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")
        print()

file_2003 = 'instructor.xls'
write03Excel(file_2003)