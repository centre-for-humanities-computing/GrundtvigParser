from TEIParser import TEIParser
from argparse import ArgumentParser
from GrundtvigTagValidator import GrundtvigTagValidator
from lxml import etree, objectify
import lxml.html, lxml.html.clean
import glob
import os
import re

class ElementFetch(TEIParser):
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

    def writeOccurences(self, directory, val_subdirectory):
        #create subdirectory if it doesn't exist
        file_dir = os.path.join(directory, val_subdirectory)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        super().write_raw(document_nodes=["content"], file_postfix="_rend", directory=file_dir)

def runFetch(input_dir, validation, output_dir):
    files = glob.glob(os.path.join(input_dir,"*.xml"), recursive=True)
    for val in validation:
        subdirectory = os.path.basename(val)[:-5]
        for f in files:
            print(f)
            try:
                #We create a TEIParser given the filename
                #Our ElementFetch will iterate through a TEI document, finding the tags
                #Specified by our validation file
                parser = ElementFetch(f) #load filename and a tag validator
                tag_valid = GrundtvigTagValidator(val)
                parser.setValidator(tag_valid)
                parser.parse(parse_text = True)
                parser.writeOccurences(output_dir, subdirectory)
                #parser.content()
            except:
                #some files do not conform to the xml standard, and are skipped
                pass

if __name__ == '__main__':
    parser = ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--idir", dest="directory",
                        help="directory containing files to be parsed", metavar="DIR", default=True, required=True)
    required.add_argument('-v','--validation', action='append', help='set one or more validation files', required=True)
    required.add_argument("-o", "--output",
                        dest="output", default=True,
                        help="Set output directory")
    args = parser.parse_args()
    validation_files = [x for x in args.validation[0].split()]
    input_directory = args.directory.strip()
    output_directory = args.output.strip()
    runFetch(input_directory, validation_files, output_directory)