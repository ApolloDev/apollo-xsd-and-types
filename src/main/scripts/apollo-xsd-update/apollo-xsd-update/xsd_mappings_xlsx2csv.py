XSD_TYPE_TO_APOLLO_SV_XLSX = "XSD Type and element to Apollo-SV mapping.xlsx"
XSD_TYPE_TO_APOLLO_SV_CSV = "xsd_type_to_apollo_sv.csv"
SHEET_NAME = "Sheet1"

def excel2CSV(ExcelFile, SheetName, CSVFile):
	import xlrd
	import csv
	workbook = xlrd.open_workbook(ExcelFile)
	worksheet = workbook.sheet_by_name(SheetName)
	csvfile = open(CSVFile, 'wb')
	wr = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

	for rownum in xrange(worksheet.nrows):
		wr.writerow(
			list(x.encode('utf-8') if type(x) == type(u'') else x
				for x in worksheet.row_values(rownum)))

	csvfile.close()
	
excel2CSV(XSD_TYPE_TO_APOLLO_SV_XLSX, SHEET_NAME, XSD_TYPE_TO_APOLLO_SV_CSV)
