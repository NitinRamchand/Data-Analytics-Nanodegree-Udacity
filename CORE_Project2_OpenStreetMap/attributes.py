'''
Created on 14 may. 2019

@author: ramchand_n
'''
import xml.etree.cElementTree as ET
from pprint import pprint

def count_attributes(filename):
    count_attributes_dict = {}
    for _, element in ET.iterparse(filename):
        for attribute in element.attrib:
            if attribute not in count_attributes_dict:
                count_attributes_dict[attribute] = 1
            else:
                count_attributes_dict[attribute] += 1
    return count_attributes_dict               
   

attributes = count_attributes('Toulouse.osm')
pprint(attributes)

