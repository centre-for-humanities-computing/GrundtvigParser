import TEIParser
import GrundtvigTagValidator
from lxml import etree, objectify
import lxml.html, lxml.html.clean
from argparse import ArgumentParser

class GruntvigParser(TEIParser):
    #Member variables
    tag_validator = None

    #Initializers
    def __init__(self, filename, tag_validator):
        super().__init__(filename)
        self.tag_validator = tag_validator

    #Public

    def metadata(self):
        return
    
    def body(self):
        return 

    def setValidator(validator):
        self.tag_validator = validator

    def extract_text(from_element):
        text = ""
    
        if from_element.text:
            text += from_element.text

        text += get_inner(from_element)

        if from_element.tail:
            text += from_element.tail
        return text
