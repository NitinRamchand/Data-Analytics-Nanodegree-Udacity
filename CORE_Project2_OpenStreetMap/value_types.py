'''
Created on 15 may. 2019

@author: ramchand_n
'''

import xml.etree.cElementTree as ET
import pprint
import re

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
capitalized = re.compile(r'([A-Z][a-z])')
     

def value_type(element, values):
    if element.tag == "tag":
        if problemchars.search(element.attrib['v']):
            values['problemchars'] += 1
        elif capitalized.search(element.attrib['v']):
            values['capitalized'] += 1
        else:
            values['other'] += 1
#            print(element.attrib['k'])

    return values


def process_map_values(filename):
    values = {"capitalized": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        values = value_type(element, values)

    return values

values = process_map_values('Toulouse.osm')
pprint.pprint(values)
