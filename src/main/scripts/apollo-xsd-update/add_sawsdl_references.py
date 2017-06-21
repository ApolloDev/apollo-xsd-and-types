import os
import csv

from modules import excel2csv

INPUT_DIR = "input_files/"
OUTPUT_DIR = "output_versions/"
XSD_TYPE_TO_APOLLO_SV_XLSX = INPUT_DIR + "XSD Type and element to Apollo-SV mapping.xlsx"
XSD_TYPE_TO_APOLLO_SV_CSV = INPUT_DIR + "xsd_types_to_apollo_sv.csv"
XSD_TO_SV_CLASS_CSV = INPUT_DIR + "Apollo-XSD-to-SV-Class-IRI.csv"
SHEET_NAME = "Sheet1"

excel2csv.excel2CSV(XSD_TYPE_TO_APOLLO_SV_XLSX, SHEET_NAME, XSD_TYPE_TO_APOLLO_SV_CSV)

with open('../../resources/apollo_types_v4.xsd', 'r+') as xsd_file:
    xsd = xsd_file.read()
    
    with open(XSD_TO_SV_CLASS_CSV) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                xsd_type = row['\xef\xbb\xbfXSD Type'].strip()
            except KeyError:
                xsd_type = row['\ufeffXSD Type'].strip()

            apollo_sv_class = row['Apollo-SB Class IRI'].strip()
            
            type_declaration = "Type name=\"" + xsd_type + "\""
            start_element_idx = xsd.index(type_declaration)
            end_element_idx = xsd.index(">", start_element_idx)
            xsd_substring = xsd[start_element_idx:end_element_idx]
            
            if "sawsdl:modelReference=" in xsd_substring:
                continue
            else:
                xsd = (xsd[:start_element_idx] + 
                xsd[start_element_idx:].replace("Type name=\"" + xsd_type + "\"", 
                "Type name=\"" + xsd_type + "\" sawsdl:modelReference=\"" + apollo_sv_class + "\""))
    
    with open(XSD_TYPE_TO_APOLLO_SV_CSV) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            xsd_type = row['XSD Element'].strip()
            apollo_sv_class = row['Apollo-SV Class IRI'].strip()
            
            type_declaration = "element name=\"" + xsd_type + "\""
            start_element_idx = xsd.index(type_declaration)
            end_element_idx = xsd.index(">", start_element_idx)
            xsd_substring = xsd[start_element_idx:end_element_idx]
            
            if "sawsdl:modelReference=" in xsd_substring:
                continue
            else:
                xsd = (xsd[:start_element_idx] + 
                xsd[start_element_idx:].replace("element name=\"" + xsd_type + "\"", 
                "element name=\"" + xsd_type + "\" sawsdl:modelReference=\"" + apollo_sv_class + "\""))
    
    num_output_files = len(os.listdir(OUTPUT_DIR))
    version = 'v%s' % (num_output_files)
    with open('%supdated_apollo_%s.xsd' % (OUTPUT_DIR, version), 'w+') as out:
        out.write(xsd)