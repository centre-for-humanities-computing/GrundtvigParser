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
from itertools import chain


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


parser = etree.XMLParser(remove_comments=True)
doc = objectify.parse("test_data.xml", parser=parser)

root = doc.getroot()
element = [x for x in root.iter("{http://www.tei-c.org/ns/1.0}p")]

print(extract_text(element[21]))
