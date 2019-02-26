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


    def extract_text(from_element):
        text = ""
        for c in list(from_element):
            if c.text:
                text += c.text
            if list(c):
                text += extract_text(c)
            if c.tail:
                text += c.tail
        return text


def is_tag(elem, tag_name):
    return etree.QName(elem.tag).localname == tag_name

def find_tag(root, tag_name, level):
    found = False
    if not is_tag(root, tag_name):
        for c in list(root):
            print(c.tag, level)
            found = find_tag2(c, tag_name, level + 1)
            if found:
                return True
    else:
        return True
    return False

def get_tag(root, tag_name=None, attribute=None, attributeValue=None, recursive=False):
        found = False
        if not is_tag(root, tag_name):
            for c in list(root):
                print(c.tag, level)
                found = find_tag2(c, tag_name, level + 1)
                if recursive:
                    return True
        else:
            return True
        return False


parser = etree.XMLParser(remove_comments=True)
documentTree = objectify.parse("test_data3.xml", parser=parser)
root = documentTree.getroot()
element = [x for x in root.iter("{http://www.tei-c.org/ns/1.0}teiHeader")]

if find_tag2(element[0], "idno", 0):
    print("NEW")
else:
    print("OLD")


#print(extract_text(element[19]))
