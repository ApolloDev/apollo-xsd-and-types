def excel2CSV(ExcelFile, SheetName, CSVFile):
    import xlrd
    import csv

    try:
        xrange
    except NameError:
        xrange = range
    
    workbook = xlrd.open_workbook(ExcelFile)
    worksheet = workbook.sheet_by_name(SheetName)
    csvfile = open(CSVFile, 'wb')
    wr = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

    for rownum in xrange(worksheet.nrows):
        wr.writerow(
            list(x.encode('utf-8') if type(x) == type(u'') else x
                for x in worksheet.row_values(rownum)))

    csvfile.close()