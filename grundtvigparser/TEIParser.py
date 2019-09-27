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
import re
import os
import json
from pathlib import Path
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
    validator
        current validator for file

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
        self.validator = None
        self.document = dict()
    
    def write_raw(self, document_nodes, file_postfix, directory=""):
        filename = Path(self.filepath).stem
        filename += file_postfix + ".txt"
        file_loc = os.path.join(directory, filename)
        with open(file_loc, "w+") as f:
            for node in document_nodes:
                for c in self.document[node]:
                    f.write(c['content'] + '\n')
    
    def write_json(self, document, file_postfix="_metadata", directory=""):
        filename = Path(self.filepath).stem
        filename += file_postfix + ".json"
        file_loc = os.path.join(directory, filename)

        j = json.dumps(document, indent=4, ensure_ascii=False)
        f = open(file_loc, 'w')
        f.write(j)

    def extract_text(self, key, from_element):
        text = ""

        #check if there is text, if so add to text
        if from_element.text:
            text += self.clean_text(from_element.text)

        #get exclusions
        #exclusions are tags that should be skipped
        excludes = self.validator.getExcludes(key, etree.QName(from_element.tag).localname)
        replaces = self.validator.getReplaces(key, etree.QName(from_element.tag).localname)

        #get inner text from inner elements
        text += self.clean_text(self.__get_inner(from_element, excludes, replaces))
        
        #check if there is tail, if so add to text
        #if from_element.tail:
        #    text += self.clean_text(from_element.tail)
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

##We now look through a hierarchy of selectors, until we get the right values. This let's us say e.g. sourceDesc > Date
    def get_elements(self, selector_path, root):
        nodes = root
        output_nodes = []
        for selector in selector_path:
            selector_array = [selector] #must be in array format to be parsed to find_Elements. Might not be best programming practice
            nodes = self.find_Elements(
                root = nodes,
                attribute = self.validator.getAttribute(selector_array),
                tag_name = self.validator.getTagName(selector_array),
                attributeValue = self.validator.getAttributeValue(selector_array),
                recursive = self.validator.getIsRecursive(selector_array)
                )
            if 'content_tag' in selector:
                #for ct in selector['content_tag']:
                nodes_found = self.find_Elements(
                    root = nodes,
                    tag_name = self.validator.getTagName(selector['content_tag']),
                    attribute = self.validator.getAttribute(selector['content_tag']),
                    attributeValue = self.validator.getAttributeValue(selector['content_tag']),
                    recursive = self.validator.getIsRecursive(selector['content_tag'])
                )
                output_nodes += nodes_found
        
        return output_nodes

    def find_Elements(self, root, tag_name=None, attribute=None, attributeValue=None, recursive=False) -> [lxml.etree.Element]:
        found_elements = []
        #go through each element in root. There may be several main tags of interest
        #e.g. get all the paragraphs and all the line groups.
        for e in root:
            if self.is_element(elem=e, tag_name=tag_name, attribute=attribute, attributeValue=attributeValue):
                found_elements += [e]
                if not recursive: #stop search if we just want the first element
                    return found_elements
        
            #Go through all elements recursively until they have all been found.
            for c in list(e):
                found_elements += self.find_Elements(
                    [c], 
                    tag_name=tag_name, 
                    attribute=attribute, 
                    attributeValue=attributeValue, 
                    recursive=recursive
                    )
                if(found_elements and not recursive):
                    return found_elements
        return found_elements
    
    def __is_tag(self, elem, tag_name):
        return etree.QName(elem.tag).localname == tag_name
    

    def setValidator(self, validator):
        self.validator = validator

    
    def clean_text(self, text):
        
        #if text.isspace():
        #    return " "
        #text = text.replace('\n', ' ')
        #text = text.replace('\t', ' ')
        
        

        #Only add spaces if the text had spaces to begin with
        #if not (text == text.strip()):
        #    if text.startswith(' ') or text.startswith('\t') and text.endswith(' ') or text.endswith('\t'):
        #        text = " " + text.strip() + " "
        #    elif text.startswith(' ') or text.startswith('\t'):
        #        text = " " + text.strip()
        #    elif text.endswith(' ') or text.endswith('\t'):
        #        text = text.strip() + " "
        re.sub("\ {2,}", " ", text)

        return text

    def __get_inner(self, from_element, excludes, replaces):
        text = ""

        #Go through all the child elements of from_element
        for c in list(from_element):
            #If elements has the attribute "facs" add a space to text. 
            #Elements with a facs attribute tend to forego spaces between tags
            if self.is_element(c, tag_name=[None], attribute=["facs"], attributeValue=[None]):
                text += " "
            
            #check whether element is in the list to exclude
            #if so, start from top
            found = False
            if excludes:
                for ex in excludes:
                    found = False
                    if self.is_element(elem=c, tag_name=[ex['tag_name']], attribute=[None], attributeValue=[None]):
                        found = True
                    if found:
                        break
            if found:
                continue
            
            if c.text:
                text += self.clean_text(c.text)
            #recursively explore for more embedded tags
            if list(c):
                text += self.__get_inner(c, excludes, replaces)
            if c.tail:
                text += self.clean_text(c.tail)

        return text

    def parse(self, parse_text = True):
        """
        Takes our root_node and our validator and extracts all of our data into a dictionary document
        
        Arguments
        ---------

        clean_text
            If True will apply text cleaning function. This may remove potential 
            metadata hidden in the formatting, but will make it neater to read.
        """

        if not self.validator:
            raise Exception("Missing validator")
            
        querySource = self.validator.getQueryTags()

        for key in querySource:
            selector_path = self.validator.getSelectorPath(key)
            elements = self.get_elements(selector_path, self.root_node)
            elements_text = []
            for e in elements:
                text = self.extract_text(key, e).strip()
                elements_text.append(
                    {
                        "tag":e, 
                        "content":text
                    })

            self.document[key] = elements_text