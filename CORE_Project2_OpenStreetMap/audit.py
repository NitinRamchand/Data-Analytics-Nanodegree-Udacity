'''
Created on 9 may. 2019

@author: RAMCHAND_N
'''
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
from pprint import pprint

OSMFILE = "Toulouse.osm"
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)
phone_number_re = re.compile(r'\+.')
phone_number_cleaning_re = re.compile(r'^\+[0-9]*')



expected_street_ascii = ["Rue", "Esplanade", "Boulevard", "Avenue", "Place", u'All\xe9e', 'Route', 'Voie', 
                   'Impasse', 'Chemin', 'Rond-Point', 'Quai', 'Promenade', 'Port', 'Passage', 'Mail',
                   'Descente', 'Clos' ]

expected_street = map(unicode,expected_street_ascii)
# UPDATE THIS VARIABLE
mapping_street = { u"route": u"Route",
            u"rue": u"Rue",
            u"rte": u"Route",
            u"esplanade": u"Esplanade",
            u"voie":u"Voie",
            u"place":u"Place",
            u"impasse":u"Impasse",
            u"chemin":u"Chemin",
            u"boulevard":u"Boulevard",
            u"avenue":u"Avenue",
            u'all\xe9es': u'All\xe9e',
            u'all\xe9e': u'All\xe9e',
            u"RUE":u"Rue",
            u"ROUTE":u"Route",
            u"Cheminement":u"Chemin",
            u"Av.":u"Avenue",
            u"Bd":u"Boulevard",
            u'All\xe9es': u'All\xe9e',
            u"AVENUE":u"Avenue",
            u"ALLEE": u'All\xe9e'
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street(osmfile):
    osm_file = open(osmfile, "r")

#    var_a = ET.iterparse(reader, events=("start",))    osm_file = open(osmfile, "r")#encoding='utf-8', errors= 'replace')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        for tag in elem.iter():
            for key in tag.attrib:
                if type(tag.attrib[key]) == str:
                    tag.attrib[key] = unicode(tag.attrib[key])
#                        print tag.attrib
#                        print type(tag.attrib[key])
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name_street(name, mapping_street):

    m = street_type_re.search(name)
    street_type = m.group()
    if m and street_type in mapping_street:
#        print 'street_type', street_type
        if street_type not in expected_street:
            name = re.sub(street_type_re, mapping_street[street_type], name)

    return name
#def update_phone(number, ):

def audit_phonenumber(no_plus_sign_phones, plus_sign_phones, actual_number):
    m = phone_number_re.search(actual_number)
    if m:
        plus_sign_phones.append(actual_number)        
    if not m:
        no_plus_sign_phones.append(actual_number)

def audit_phone(osmfile):
    osm_file = open(osmfile, "r")
    no_plus_sign_phones = []
    plus_sign_phones = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        for tag in elem.iter():
            for key in tag.attrib:
                if type(tag.attrib[key]) == str:
                    tag.attrib[key] = unicode(tag.attrib[key])
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                if (tag.attrib['k'] == "phone") or (tag.attrib['k'] == "contact:phone"):
                    audit_phonenumber(no_plus_sign_phones, plus_sign_phones, actual_number=tag.attrib['v'])
    osm_file.close()
    return no_plus_sign_phones, plus_sign_phones

def updated_phonenumber_format(OSMFILE):    
    no_plus_sign_phones, plus_sign_phones = audit_phone(OSMFILE)
    for plus_sign_phone in plus_sign_phones:
        m = phone_number_cleaning_re.search(plus_sign_phone)
        if m:
            updated_number_step1 = re.sub(r'^\+','00',plus_sign_phone)
            updated_number = re.sub(r'[\D|\s]+','',updated_number_step1)            
            print plus_sign_phone,"=>", updated_number
    for no_plus_sign_phone in no_plus_sign_phones:
        if no_plus_sign_phone == u'3631':
            updated_number = u'0033972721213'
            print no_plus_sign_phone,"=>", updated_number
        else:
            phone_number_start_0_re = re.compile(r'^[0]')
            phone_number_start_0_re = re.compile(r'^[0]')
            match_phone = phone_number_start_0_re.match(no_plus_sign_phone)
            match_phone = phone_number_start_0_re.match(no_plus_sign_phone)
            if match_phone:
                updated_number_step1 = re.sub(r'^[0]','0033',no_plus_sign_phone)
                updated_number = re.sub(r'[\D|\s]+','',updated_number_step1)
                print no_plus_sign_phone,"=>", updated_number
            else:
                updated_number_step1 = re.sub(r'^[3]','003',no_plus_sign_phone)
                updated_number = re.sub(r'[\D|\s]+','',updated_number_step1)
                print no_plus_sign_phone,"=>", updated_number
    
            
    

def test():
    
    no_plus_sign_phones, plus_sign_phones = audit_phone(OSMFILE)
#    pprint(no_plus_sign_phones)
#    pprint(plus_sign_phones)
#    pprint(dict(st_types))

    updated_phonenumber_format(OSMFILE)
    st_types = audit_street(OSMFILE)
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name_street(name, mapping_street)
            print name, "=>", better_name

if __name__ == '__main__':
    mydict= test()