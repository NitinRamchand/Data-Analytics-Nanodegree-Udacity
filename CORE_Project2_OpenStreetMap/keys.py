'''
Created on 14 may. 2019

@author: ramchand_n
'''
import xml.etree.cElementTree as ET
from pprint import pprint

def types_keys(filename):
    types_keys_dict = {}
    for event, element in ET.iterparse(filename, events=("start","end")):
        if event == "start":
            for tag in element.iter("tag"):
                key = tag.attrib['k']
                if key not in types_keys_dict:
                    types_keys_dict[key] = 1
                else:
                    types_keys_dict[key] += 1
    return types_keys_dict               
   

keys = types_keys('Toulouse.osm')
pprint(keys)

