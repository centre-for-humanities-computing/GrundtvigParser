from TEIParser import TEIParser
from GrundtvigTagValidator import GrundtvigTagValidator
from lxml import etree, objectify
import lxml.html, lxml.html.clean
from argparse import ArgumentParser
import glob
import os
import re


class GrundtvigParser(TEIParser):
    """
    Derived TEIParser class for parsing Grundtvig data

    Attributes
    ------------
    root_node
        the base node for the file
    filepath
        the filepath of the TEI file

    Methods
    ------------
    metadata
        gets all text within all tags starting at the first element
    content
        boolean value indicating wether the element with tag exists
    setValidator
        sets a tag validator
    extract_text
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

    def __init__(self, filename):
        super().__init__(filename)
        self.tag_validator = None

    def metadata(self):
        return
    
    def content(self):
        tags = self.tag_validator.getQueryTags("body")

        #We need to get the content from the body tag
        content_base = super().get_Elements(
            [self.root_node], 
            tag_name=["body"], 
            attribute=[None], 
            attributeValue=[None], 
            recursive=False
            )

        #Once we gave the body element, we can find all the elements
        content = super().get_Elements(
            content_base[0], 
            tag_name=self.tag_validator.getTagName(tags), 
            attribute=self.tag_validator.getAttribute(tags),
            attributeValue=self.tag_validator.getAttributeValue(tags),
            recursive=self.tag_validator.getIsRecursive(tags)
            )

        text = ""
        for c in content:
            text += self.clean_text(self.extract_text(c[0],tags)) + '\n\n'
        
        text = re.sub(",", ", ", text)
        text = re.sub("\ {2,}", " ", text)
        open("../grundtvig-data/Data/raw_ubehandledeFiler/"+os.path.basename(self.filepath)+".txt", "w+").write(text)


    def setValidator(self, validator):
        self.tag_validator = validator

    
    def extract_text(self, from_element, t):
        text = ""
        #check if there is text, if so add to text
        if from_element.text:
            text += self.clean_text(from_element.text.strip())

        #get exclusions
        #exclusions are tags that should be skipped
        excludes = self.tag_validator.getExcludes(self.tag_validator.getElementForTagName(t, etree.QName(from_element.tag).localname))

        #get inner text from inner elements
        text += self.clean_text(self.__get_inner(from_element, excludes))
       
        #check if there is tail, if so add to text
        if from_element.tail:
            text += self.clean_text(from_element.tail.strip())
        return text

    def clean_text(self, text):
        if text.isspace():
            return " "
        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')

        #Only add spaces if the text had spaces to begin with
        if not (text == text.strip()):
            if text.startswith(' ') or text.startswith('\t') and text.endswith(' ') or text.endswith('\t'):
                text = " " + text.strip() + " "
            elif text.startswith(' ') or text.startswith('\t'):
                text = " " + text.strip()
            elif text.endswith(' ') or text.endswith('\t'):
                text = text.strip() + " "

        return text

    def __get_inner(self, from_element, excludes):
        text = ""

        #Go through all the child elements of from_element
        for c in list(from_element):
            #If elements has the attribute "facs" add a space to text. 
            #Elements with a facs attribute tend to forego spaces between tags
            if super().is_element(c, tag_name=[None], attribute=["facs"], attributeValue=[None]):
                text += " "
            
            #check whether element is in the list to exclude
            #if so, start from top
            found = False
            if excludes:
                for ex in excludes:
                    found = False
                    if super().is_element(elem=c, tag_name=[ex['tag_name']], attribute=[None], attributeValue=[None]):
                        found = True
                if found:
                    continue
            
            if c.text:
                text += self.clean_text(c.text)
            #recursively explore for more embedded tags
            if list(c):
                text += self.__get_inner(c, excludes)
            if c.tail:
                text += self.clean_text(c.tail)

        return text



#Find and iterate through all the files
files = glob.iglob("../grundtvig-data/Data/ubehandledeFiler/*.xml", recursive=True)
for f in files:
    try:
        #We create a TEIParser given the filename
        #Our GrundtvigParser will iterate through a TEI document, finding the tags
        #Specified by our GrundtvigTagValidator object
        parser = GrundtvigParser(f) #load filename and a tag validator
        #Check the version, adjust validator based on version
        if parser.find_tag(parser.root_node, "idno"):
            tag_valid = GrundtvigTagValidator("grundtvig-new.json")
            parser.setValidator(tag_valid)

        else:
            tag_valid = GrundtvigTagValidator("grundtvig-new.json")
            parser.setValidator(tag_valid)
        #content of files are retrieved and saved
        #TODO: Add modular saving function
        parser.content()
    except:
        #some files do not conform to the xml standard, and are skipped
        pass