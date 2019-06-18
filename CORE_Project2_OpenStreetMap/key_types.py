'''
Created on 9 may. 2019

@author: RAMCHAND_N
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

# def is_street_name(elem):
#     return (elem.attrib['k'] == "addr:street")
# 
# 
# def audit():
#     for event, elem in ET.iterparse("Compans_Caffarelli.osm", events=("start",)):
#         if elem.tag == "way":
#             for tag in elem.iter("tag"):
#                 if is_street_name(tag):
#                     audit_street_type(street_types, tag.attrib['v'])
#     pprint.pprint(dict(street_types))

# 
# Your task is to explore the data a bit more.
# Before you process the data and add it into your database, you should check the
# "k" value for each "<tag>" and see if there are any potential problems.
# 
# We have provided you with 3 regular expressions to check for certain patterns
# in the tags. As we saw in the quiz earlier, we would like to change the data
# model and expand the "addr:street" type of keys to a dictionary like this:
# {"address": {"street": "Some value"}}
# So, we have to see if we have such tags, and if we have any tags with
# problematic characters.
# 
# Please complete the function 'key_type', such that we have a count of each of
# four tag categories in a dictionary:
#   "lower", for tags that contain only lowercase letters and are valid,
#   "lower_colon", for otherwise valid tags with a colon in their names,
#   "problemchars", for tags with problematic characters, and
#   "other", for other tags that do not fall into the other three categories.
# See the 'process_map' and 'test' functions for examples of the expected format.
# The following function __key_types()__ looks through all tags called "tag" and puts the 'k' attribute into the following different categories and the occurences of them:
# - "lowercase", for tags that contain only lowercase letters and are valid,
# - "lowercase_colon", for otherwise valid tags with a colon in their names,
# - "lowercase_semicolon", for otherwise valid tags with a semicolon in their names,
# - "lowercase_morethanone_colon", for tags with at least two semicolons in their names,
# - "capitalized", for tags starting with a capital letter,
# - "problemchars", for tags with problematic characters, and
# - "other", for other tags that do not fall into the other three categories.
# """




lowercase = re.compile(r'^([a-z]|_)*$')
lowercase_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
lowercase_semicolon = re.compile(r'^([a-z]|_)*;([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
capitalized = re.compile(r'([A-Z][a-z])')
lowercase_morethanone_colon = re.compile(r'^((:*){2,})')
     

def key_type(element, keys):
    if element.tag == "tag":
        if lowercase.search(element.attrib['k']):
            keys['lowercase'] += 1
        elif lowercase_colon.search(element.attrib['k']):
            keys['lowercase_colon'] += 1
        elif capitalized.search(element.attrib['k']):
            keys['capitalized'] += 1
        elif lowercase_morethanone_colon.search(element.attrib['k']):
            keys['lowercase_morethanone_colon'] += 1
        elif lowercase_semicolon.search(element.attrib['k']):
            keys['lowercase_semicolon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
#            print(element.attrib['k'])

    return keys


def process_map_keys(filename):
    keys = {"lowercase": 0, "lowercase_colon": 0, "lowercase_morethanone_colon": 0,"lowercase_semicolon": 0, "capitalized": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map_keys('Toulouse.osm')
    pprint.pprint(keys)
#    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()