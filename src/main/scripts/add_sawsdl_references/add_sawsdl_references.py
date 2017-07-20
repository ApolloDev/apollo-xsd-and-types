import os
import csv
import sys

import urllib.request
import xmltodict

from modules import excel2csv
from collections import OrderedDict

INPUT_DIR = "input_files/"
OUTPUT_DIR = "output_versions/"
MAPPINGS_XLSX = INPUT_DIR + "Apollo-XSD-to-Classes-mappings.xlsx"
SHEETS = ["Apollo Types", "Apollo Elements"]
APOLLO_SV = "apollo-sv.owl"

for SHEET in SHEETS:
    excel2csv.excel2CSV(MAPPINGS_XLSX, SHEET, INPUT_DIR + SHEET + ".csv")

def get_desc_from_obj(desc_obj):
    if isinstance(desc_obj, str):
        return desc_obj
    elif isinstance(desc_obj, OrderedDict):
        return desc_obj["#text"]
    elif isinstance(desc_obj, list):
        return get_desc_from_obj(desc_obj[0])

apollo_sv_desc = {}
with open(INPUT_DIR + APOLLO_SV) as apollo_sv:
    sv_content = apollo_sv.read()
    sv_dict = xmltodict.parse(sv_content)['rdf:RDF']
    keys = sv_dict.keys()

    annotation_property = 'obo:IAO_0000115'
    for key in keys:
        for item in sv_dict[key]:
            if annotation_property in item:
                item_name = item['@rdf:about']
                desc_obj = item[annotation_property]
                description = get_desc_from_obj(desc_obj)

                apollo_sv_desc[item_name] = description

class purlHTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print(fp.getcode())
        print(fp.geturl())
        
        return urllib.request.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

def csv_to_xsd(csv_file, xsd, fields, declaration):
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        xsd_type = row[fields[0]].strip()
        apollo_sv_class = row[fields[1]].strip()
        
        if len(sys.argv) == 1 or not (len(sys.argv) > 1 
            and sys.argv[1] == '-s' or sys.argv[1] == '--skipUrlValidation'):
            try:
                response = urllib.request.urlopen(apollo_sv_class)
                if response.getcode() != 200:
                    print(response.getcode())
                    print(apollo_sv_class)
                
            except urllib.error.HTTPError as http_error:
                print(http_error.code)
                print(apollo_sv_class)
        
        full_declaration = declaration + xsd_type + "\""
        start_element_idx = xsd.index(full_declaration)
        end_element_idx = xsd.index(">", start_element_idx)
        xsd_substring = xsd[start_element_idx:end_element_idx]
        
        if "sawsdl:modelReference=" in xsd_substring:
            continue
        else:
            if apollo_sv_class in apollo_sv_desc:
                documentation_str = ('>\n<annotation>\n<documentation>\n' + 
                    apollo_sv_desc[apollo_sv_class] + '\n</documentation>\n</annotation>')
                if xsd_substring.endswith('/'):
                    full_element = xsd[start_element_idx-10:end_element_idx].strip()
                    element_name = full_element[full_element.index('<') + 1:full_element.index(' ')]
                    xsd = (xsd[:end_element_idx-1] + documentation_str + 
                        '\n</' + element_name + '>\n' + xsd[end_element_idx+1:])
                else:
                    xsd = (xsd[:end_element_idx] + documentation_str + xsd[end_element_idx+1:])

            xsd = (xsd[:start_element_idx] + 
            xsd[start_element_idx:].replace(declaration + xsd_type + "\"", 
            declaration + xsd_type + "\" sawsdl:modelReference=\"" + apollo_sv_class + "\""))

    return xsd

opener = urllib.request.build_opener(purlHTTPRedirectHandler)
urllib.request.install_opener(opener)

with open('../../resources/apollo_types_v4_template.xsd', 'r+') as xsd_file:
    xsd = xsd_file.read()
    
    with open(INPUT_DIR + SHEETS[0] + '.csv') as csv_file:
        fields = ['XSD Type', 'Apollo-SB Class IRI']
        declaration = "Type name=\""
        xsd = csv_to_xsd(csv_file, xsd, fields, declaration)
    
    with open(INPUT_DIR + SHEETS[1] + '.csv') as csv_file:
        fields = ['XSD Element', 'Apollo-SV Class IRI']
        declaration = "element name=\""
        xsd = csv_to_xsd(csv_file, xsd, fields, declaration)

    num_output_files = len(os.listdir(OUTPUT_DIR))
    #version = 'v%s' % (num_output_files)
    version = 'v6'
    with open('%supdated_apollo_%s.xsd' % (OUTPUT_DIR, version), 'w+') as out:
        out.write(xsd)
