def excel2CSV(ExcelFile, SheetName, CSVFile):
    import xlrd
    import csv
    
    workbook = xlrd.open_workbook(ExcelFile)
    worksheet = workbook.sheet_by_name(SheetName)
    csvfile = open(CSVFile, 'w')
    csvWriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    
    for rownum in range(worksheet.nrows):
        #this commented block only works in python 2.7
        #in python 2.7 type(u'') is <type 'unicode'> but in python 3.6 it is <type 'str'>
        #csvWriter.writerow(
            #list(
                #x.encode('utf-8') if type(x) == type(u'') else x
                #    for x in worksheet.row_values(rownum)
            #)
        #)
        
        csvWriter.writerow(worksheet.row_values(rownum))
    
    csvfile.close()
