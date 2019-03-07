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

class TEIParser:
    """
    Class for parsing TEI files

    Attributes
    ------------
    root_node
        the base node for the file
    filepath
        the filepath of the TEI file

    Methods
    ------------
    extract_text
        gets all text within all tags starting at the first element
    find_tag
        boolean value indicating wether the element with tag exists
    is_element
        boolean value indicating whether element has tag, attribute and attribute value
    get_Elements
        returns all elements that match description
    write_json
        writes files to json
    write_raw
        writes raw document to file
    __get_inner
        scans elements
    __is_tag
        returns wether tag is actual tag
    """
    root_node = None
    def __init__(self, filename):
        parser = etree.XMLParser(remove_comments=True)
        documentTree = objectify.parse(filename, parser=parser)
        self.root_node = documentTree.getroot()   
        self.filepath = filename 
   

    #Public variables:
    def extract_text(self, from_element):
        text = ""
        #check if there is text, if so add to text
        if from_element.text:
            text += from_element.text

        #get inner text from inner elements
        text += self.__get_inner(from_element)

        #check if there is tail, if so add to text
        if from_element.tail:
            text += from_element.tail
        return text

    def find_tag(self, root, tag_name) -> bool:
        found = False
        if not self.__is_tag(root, tag_name):
            for c in list(root):
                found = self.find_tag(c, tag_name)
                if found:
                    return True
        else:
            return True
        return False

    def is_element(self, elem, tag_name=None, attribute=None, attributeValue=None) -> bool:
        found = True
        #check through both tag_name, attribute and attributeValue for each element at the same timee
        #Adjusts output based on which elements aren't null
        for tg, at, av in zip(tag_name, attribute, attributeValue):
            if(tg and at and av):
                found =  etree.QName(elem.tag).localname == tg and (at in elem.attrib) and elem.attrib[at] == av
            elif tg and at:
                found = etree.QName(elem.tag).localname == tg and (at in elem.attrib)
            elif  tg and av:
                found = etree.QName(elem.tag).localname == tg and elem.attrib.values[0] == av
            elif at and av:
                found = elem.attrib[at] and elem.attrib.values[0] == av
            elif tg:
                found = etree.QName(elem.tag).localname == tg
            elif at:
                found = (at in elem.attrib)
            elif av:
                found = elem.attrib.values[0] == av
            if found:
                return found
        return found


    def get_Elements(self, root, tag_name=None, attribute=None, attributeValue=None, recursive=False) -> [lxml.etree.Element]:
        found_elements = []
        #go through each element in root. There may be several main tags of interest
        #i.e. get all the paragraphs and all the line groups.
        for e in root:
            if self.is_element(elem=e, tag_name=tag_name, attribute=attribute, attributeValue=attributeValue):
                found_elements += [root]
                if not recursive: #stop search if we just want the first element
                    return found_elements
        
            #Go through all elements recursively until they have all been found.
            for c in list(e):
                found_elements += self.get_Elements([c], tag_name=tag_name, attribute=attribute, attributeValue=attributeValue, recursive=recursive)
                if(found_elements and not recursive):
                    return found_elements
            return found_elements
    
    def write_json(self):
        return
    def write_raw(self, sep='\n'):
        return
    
    #Private functions
    def __get_inner(self, from_element):
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
    
    def __is_tag(self, elem, tag_name):
        return etree.QName(elem.tag).localname == tag_name