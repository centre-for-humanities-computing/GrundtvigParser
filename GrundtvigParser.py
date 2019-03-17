from TEIParser import TEIParser
from GrundtvigTagValidator import GrundtvigTagValidator
from lxml import etree, objectify
import lxml.html, lxml.html.clean
from argparse import ArgumentParser
import glob
from glob import iglob
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

    """
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
"""

#Find and iterate through all the files
files = iglob("/Users/oliverjarvis/Arbejde/grundtvig-data/Data/xmlFilesEdit/1804-1825/*.xml", recursive=True)

for f in files:
    print(f)
    f1 = "/Users/oliverjarvis/Arbejde/grundtvig-parser/test_data.xml"
    try:
        #We create a TEIParser given the filename
        #Our GrundtvigParser will iterate through a TEI document, finding the tags
        #Specified by our GrundtvigTagValidator object
        parser = GrundtvigParser(f1) #load filename and a tag validator
        #Check the version, adjust validator based on version
        if parser.find_tag(parser.root_node, "idno"):
            tag_valid = GrundtvigTagValidator("/Users/oliverjarvis/Arbejde/grundtvig-parser/grundtvig-tagvalid.json")
            parser.setValidator(tag_valid)
            parser.parse()

        else:
            tag_valid = GrundtvigTagValidator("/Users/oliverjarvis/Arbejde/grundtvig-parser/grundtvig-tagvalid.json")
            parser.setValidator(tag_valid)
            parser.parse()
        #content of files are retrieved and saved
        #TODO: Add modular saving function
        #parser.content()
    except:
        #some files do not conform to the xml standard, and are skipped
        pass