import os
import csv

import urllib.request

from modules import excel2csv

INPUT_DIR = "input_files/"
OUTPUT_DIR = "output_versions/"
#XSD_TYPE_TO_APOLLO_SV_XLSX = INPUT_DIR + "XSD Type and element to Apollo-SV mapping.xlsx"
#XSD_TYPE_TO_APOLLO_SV_CSV = INPUT_DIR + "xsd_types_to_apollo_sv.csv"
#XSD_TO_SV_CLASS_CSV = INPUT_DIR + "Apollo-XSD-to-SV-Class-IRI.csv"
#SHEET_NAME = "Sheet1"
MAPPINGS_XLSX = INPUT_DIR + "Apollo-XSD-to-Classes-mappings.xlsx"
SHEETS = ["Apollo Types", "Apollo Elements"]

for SHEET in SHEETS:
    excel2csv.excel2CSV(MAPPINGS_XLSX, SHEET, INPUT_DIR + SHEET + ".csv")

class purlHTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print(fp.getcode())
        print(fp.geturl())
        
        return urllib.request.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

opener = urllib.request.build_opener(purlHTTPRedirectHandler)
urllib.request.install_opener(opener)

with open('../../resources/apollo_types_v4.xsd', 'r+') as xsd_file:
    xsd = xsd_file.read()
    
    with open(INPUT_DIR + SHEETS[0] + '.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            xsd_type = row['XSD Type'].strip()
            apollo_sv_class = row['Apollo-SB Class IRI'].strip()
            
            try:
                response = urllib.request.urlopen(apollo_sv_class)
                if response.getcode() != 200:
                    print(response.getcode())
                    print(apollo_sv_class)
                
            except urllib.error.HTTPError as http_error:
                print(http_error.code)
                print(apollo_sv_class)
            
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
    
    with open(INPUT_DIR + SHEETS[1] + '.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            xsd_type = row['XSD Element'].strip()
            apollo_sv_class = row['Apollo-SV Class IRI'].strip()
            
            try:
                response = urllib.request.urlopen(apollo_sv_class)
                if response.getcode() != 200:
                    print(response.getcode())
                    print(apollo_sv_class)
                
            except urllib.error.HTTPError as http_error:
                print(http_error.code)
                print(apollo_sv_class)
            
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
