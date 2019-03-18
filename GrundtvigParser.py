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

    def getMetadata(self):
        metadata_document = dict()

        #get status
        status = ""
        if super().find_tag(parser.root_node, "idno"):
            status = "behandlet"
        else:
            status = "ubenhandlet"

        metadata_document['status'] = status

        #get filename:
        metadata_document['file'] = os.path.basename(self.filepath)
        metadata_document['date'] = self.document['date'][0]['content']


        if metadata_document['status'] == "behandlet":

            metadata_document['version_id'] = self.document['version'][0]['content']
            #get genre
            genres = ""
            for x in self.document['genre']:
                genres += x['content'] + " "
            
            metadata_document['genres'] = genres
            #get keywords
            keywords = ""
            for x in self.document['keywords']:
                keywords += x['content'] + " "
            metadata_document['keywords'] = keywords

        super().write_json(metadata_document)
        
    def getContent(self):
        super().write_raw(document_nodes=["content"], file_prefix="clean_")

        

    def write_json(self):
        return

#Find and iterate through all the files
files = iglob("/Users/oliverjarvis/Arbejde/grundtvig-data/Data/xmlFilesEdit/1804-1825/*.xml", recursive=True)

for f in files:
    f1 = "/Users/oliverjarvis/Arbejde/grundtvig-parser/test_data_old.xml"
    try:
        #We create a TEIParser given the filename
        #Our GrundtvigParser will iterate through a TEI document, finding the tags
        #Specified by our GrundtvigTagValidator object
        parser = GrundtvigParser(f1) #load filename and a tag validator
        #Check the version, adjust validator based on version
        if parser.find_tag(parser.root_node, "idno"):
            tag_valid = GrundtvigTagValidator("/Users/oliverjarvis/Arbejde/grundtvig-parser/grundtvig-tagvalid.json")
            parser.setValidator(tag_valid)
            parser.parse(parse_text = True)
            parser.getMetadata()

        else:
            tag_valid = GrundtvigTagValidator("/Users/oliverjarvis/Arbejde/grundtvig-parser/grundtvig-tagvalid-old.json")
            parser.setValidator(tag_valid)
            parser.parse()
            parser.getMetadata()
            parser.getContent()
        #content of files are retrieved and saved
        #TODO: Add modular saving function
        #parser.content()
    except:
        #some files do not conform to the xml standard, and are skipped
        pass