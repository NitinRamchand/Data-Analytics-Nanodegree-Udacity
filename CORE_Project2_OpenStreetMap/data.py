'''
Created on 24 may. 2019

@author: ramchand_n
'''
import xml.etree.cElementTree as ET
import re
from pprint import pprint
from collections import defaultdict
import codecs
import json


#OSMFILE = "Toulouse.osm"
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)
phone_number_re = re.compile(r'\+.')
phone_number_cleaning_re = re.compile(r'^\+[0-9]*')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

expected_street_ascii = ["Rue", "Esplanade", "Boulevard", "Avenue", "Place", u'All\xe9e', 'Route', 'Voie', 
                   'Impasse', 'Chemin', 'Rond-Point', 'Quai', 'Promenade', 'Port', 'Passage', 'Mail',
                   'Descente', 'Clos' ]

expected_street = map(unicode,expected_street_ascii)

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

def audit_phonenumber(no_plus_sign_phones, plus_sign_phones, actual_number):
    m = phone_number_re.search(actual_number)
    if m:
        plus_sign_phones.append(actual_number)        
    if not m:
        no_plus_sign_phones.append(actual_number)
    return no_plus_sign_phones, plus_sign_phones
     
def update_name_street(name, mapping_street):

    m = street_type_re.search(name)
    street_type = m.group()
    if m and street_type in mapping_street:
#        print 'street_type', street_type
        if street_type not in expected_street:
            name = re.sub(street_type_re, mapping_street[street_type], name)

    return name

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street:
            street_types[street_type].add(street_name)
    return street_types
    
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag

        # Parse attributes
        for a in element.attrib:
            if a in CREATED:
                if 'created' not in node:
                    node['created'] = {}
                node['created'][a] = element.attrib[a]

            elif a in ['lat', 'lon']:
                if 'pos' not in node:
                    node['pos'] = [None, None]
                if a == 'lat':
                    node['pos'][0] = float(element.attrib[a])
                else:
                    node['pos'][1] = float(element.attrib[a])

            else:
                node[a] = element.attrib[a]

        # Iterate tag children
        for tag in element.iter("tag"):
            if (tag.attrib['k'] == "addr:street"):
                for st_type, ways in st_types.iteritems():
                            for name in ways:
                                if 'address' not in node:
                                    node['address'] = {}
                                node['address']['street'] = update_name_street(name, mapping_street)
 #                               print (update_name_street(name, mapping_street))
#                                pprint (node)      
            # Single colon beginning with addr
            elif tag.attrib['k'].find('addr:') == 0:
                if 'address' not in node:
                    node['address'] = {}      
                sub_attr = tag.attrib['k'].split(':', 1)
                node['address'][sub_attr[1]] = tag.attrib['v']
#                        pprint (node)
#                pprint (node)
            elif (tag.attrib['k'] == "phone") or (tag.attrib['k'] == "contact:phone") or (tag.attrib['k'] == "contact:fax"):                
                for plus_sign_phone in plus_sign_phones:
                    m = phone_number_cleaning_re.search(plus_sign_phone)
                    if m:
                        updated_number_step1 = re.sub(r'^\+','00',plus_sign_phone)
                        node['phone'] = re.sub(r'[\D|\s]+','',updated_number_step1)
#                        pprint (node)            
                 #       print plus_sign_phone,"=>", updated_number
                for no_plus_sign_phone in no_plus_sign_phones:
                    if no_plus_sign_phone == u'3631':
                        node['phone'] = u'0033972721213'
#                        pprint (node)   
                 #       print no_plus_sign_phone,"=>", updated_number
                    else:
                        phone_number_start_0_re = re.compile(r'^[0]')
                        phone_number_start_0_re = re.compile(r'^[0]')
                        match_phone = phone_number_start_0_re.match(no_plus_sign_phone)
                        match_phone = phone_number_start_0_re.match(no_plus_sign_phone)
                        if match_phone:
                            updated_number_step1 = re.sub(r'^[0]','0033',no_plus_sign_phone)
                            node['phone'] = re.sub(r'[\D|\s]+','',updated_number_step1)
                 #           print no_plus_sign_phone,"=>", updated_number
                        else:
                            updated_number_step1 = re.sub(r'^[3]','003',no_plus_sign_phone)
                            node['phone'] = re.sub(r'[\D|\s]+','',updated_number_step1)
#                    pprint (node)      

            else:
                node[tag.attrib['k']] = tag.attrib['v']
#                pprint (node)      

        for nd in element.iter("nd"):
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'].append(nd.attrib['ref'])
#        pprint (node)
        return node
    else:
        return None
    
    
file_out = "Toulouse.json"
with codecs.open(file_out, "w") as fo:
    #fo.write('[')
    data = []
    street_types = defaultdict(set)
    no_plus_sign_phones = []
    plus_sign_phones = []
    for event, elem in ET.iterparse('Toulouse.osm', events=("start",)):
        for tag in elem.iter():
            for key in tag.attrib:
                if type(tag.attrib[key]) == str:
                    tag.attrib[key] = unicode(tag.attrib[key])
                    
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                if (tag.attrib['k'] == "phone") or (tag.attrib['k'] == "contact:phone") or (tag.attrib['k'] == "contact:fax"):                
                    no_plus_sign_phones, plus_sign_phones = audit_phonenumber(no_plus_sign_phones, plus_sign_phones, actual_number=tag.attrib['v'])
                elif (tag.attrib['k'] == "addr:street"):
                    st_types = audit_street_type(street_types, street_name=tag.attrib['v']) 
        el = shape_element(elem)
        if el:
            data.append(el)
            #fo.write(json.dumps(el) + "\n")
    fo.write(json.dumps(data))
    #fo.write(']')

