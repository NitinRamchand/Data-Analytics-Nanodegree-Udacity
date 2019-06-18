'''
Created on 14 may. 2019

@author: ramchand_n
'''
import xml.etree.cElementTree as ET
from pprint import pprint

def types_values(filename):
    types_values_dict = {}
    for event, element in ET.iterparse(filename, events=("start","end")):
        if event == "start":
            for tag in element.iter("tag"):
                value = tag.attrib['v']
                if value not in types_values_dict:
                    types_values_dict[value] = 1
                else:
                    types_values_dict[value] += 1
    return types_values_dict               
   

values = types_values('Toulouse.osm')
pprint(values)

