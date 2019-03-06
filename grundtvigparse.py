##The grundtvig parser##
#This software has been created to parse grundtvig center
#data into a format that is machine readible for text analysis
#Software outputs <FILENAME>.metadata for metadata
#                 <FILENAME>.parsed.txt for parsed text
#Created by Oliver Jarvis
#Organization: CHCAA
#Website: CHCAA.ai

#get list of relevant elements
#recursively extract the text until there is not left
#Start at the inner element return text at that location
#insert text into general string and then run lxml again on that text

#create a tag validator. What tags are allowed, which are dissallowed,
#pass it version number and return allowed tags and allowed children.
#


#find tags
#get tags
#create system with json files describing the structure of meta data and content

from lxml import etree, objectify
import lxml.html, lxml.html.clean
from argparse import ArgumentParser
#from GrundtvigTagValidator import metadata, body

class GrundtvigParse:
    #""" The main parser for grundtvig data"""
    documentTree = None
    def __init__(self, filename):

        parse(filename)

    #def getVersionNumber
    def parse(self, filename, remove_comments=True):
    #"""parse(filename, parser, remove_comments=True) filename = file to open for parsing parser = XMLParser() remove_comments = bool keep xml comments"""
        parser = etree.XMLParser(remove_comments=remove_comments)
        documentTree = objectify.parse("test_data.xml", parser=parser).getroot()

    def metadata():
    #""" def matadata()
    #    get metadata in dictionary format
    #"""
        if(documentTree):
            rootTag = getHead()
            metadataDict = extractText(rootTag, validateTag.metadata, raw_text=False)

def get_inner(from_element):
    text = ""
    for c in list(from_element):
        if is_element(c, attribute="facs"):
            text += " "
        if tagIsAccepted(c.tag):
            if c.text:
                text += c.text
            if list(c):
                text += get_inner(c)
            if c.tail:
                text += c.tail
        

            
    return text

def extract_text(from_element):
    text = ""
  
    if from_element.text:
        text += from_element.text

    text += get_inner(from_element)

    if from_element.tail:
        text += from_element.tail
    return text


def is_tag(elem, tag_name):
    return etree.QName(elem.tag).localname == tag_name

def find_tag(root, tag_name):
    found = False
    if not is_tag(root, tag_name):
        for c in list(root):
            found = find_tag(c, tag_name)
            if found:
                return True
    else:
        return True
    return False

def tagIsAccepted(tag):
    atag = etree.QName(tag).localname
    if atag != "witDetail" and atag != "rdg": return True
    return False

def is_element(elem, tag_name=None, attribute=None, attributeValue=None):
    if(tag_name and attribute and attributeValue):
        return etree.QName(elem.tag).localname == tag_name and (attribute in elem.attrib) and elem.attrib[attribute] == attributeValue
    if tag_name and attribute:
        return etree.QName(elem.tag).localname == tag_name and (attribute in elem.attrib)
    if  tag_name and attributeValue:
        return etree.QName(elem.tag).localname == tag_name and elem.attrib.values[0] == attributeValue
    if attribute and attributeValue:
        return elem.attrib[attribute] and elem.attrib.values[0] == attributeValue
    if tag_name:
        return etree.QName(elem.tag).localname == tag_name
    if attribute:
        return (attribute in elem.attrib)
    if attributeValue:
        return elem.attrib.values[0] == attributeValue
    else:
        return True

def get_Elements(root, tag_name=None, attribute=None, attributeValue=None, recursive=False):
        found_elements = []
        #remember tag name
        if is_element(root, tag_name=tag_name, attribute=attribute, attributeValue=attributeValue):
            found_elements += [root]
            if not recursive:
                return found_elements

        for c in list(root):
            found_elements += get_Elements(c, tag_name=tag_name, attribute=attribute, attributeValue=attributeValue, recursive=recursive)
            if(found_elements and not recursive):
                return found_elements
        return found_elements


parser = etree.XMLParser(remove_comments=True)
documentTree = objectify.parse("test_data.xml", parser=parser)
root = documentTree.getroot()


element = [x for x in root.iter("{http://www.tei-c.org/ns/1.0}teiHeader")]
if find_tag(element[0], "idno"):
    print("NEW")
else:
    print("OLD")


header = get_Elements(root, tag_name="teiHeader", recursive=False)
print(header)



body = get_Elements(root, tag_name="body", recursive=False)
print(body)
paragraphs = get_Elements(body[0], tag_name="p", recursive=True)

alltext = "" 

for x in paragraphs:
    alltext += extract_text(x).strip() + '\n'

f = open("alltext.txt", "w+")
f.write(alltext)

# print(extract_text(element[19]))