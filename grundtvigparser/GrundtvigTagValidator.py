""" Collects acceptable tags and their hierachies """
import json

class GrundtvigTagValidator:
    """
    A class that receives a validation file, and parses/outputs its contents

    Attributes
    ------------
    tagValidator: dict
        Stores the validation file in a dictionary format

    Methods
    ------------    
    getQueryTags
        Finds the category tags. Different categories of content may reside
        within certain tags. e.g. We may want to only get metadata, these may
        be stores within a certain tag (e.g. <header/>)
    getElementForTagName
        Gets the validation element for a certain Tag
    getExcludes
        Gets the tags to exclude for a particular Tag
    getTagName
        Gets the tag_names for a certain content category (i.e. metadata, main content, etc.)
    getAttribute
        Gets the attributes for a certain content category 
    getAttributeValue
        Gets the attribute values for a certain content category
    getIsRecursive
        Gets the boolean recursion value #TODO
    """
    def __init__(self, validatorFile):
        self.tagValidator = json.loads(open(validatorFile).read())
    
    def getQueryTags(self):
        return list(self.tagValidator.keys())

    #def getQueryTags(self,query):
    #    return self.tagValidator['tags'][query]

    def getSelectorPath(self, key):
        if key in self.tagValidator:
            if 'selector_path' in self.tagValidator[key]:
                return self.tagValidator[key]['selector_path']
        else:
            raise Exception("Error: Key or selector_path missing.")

    def getElementForTagName(self, elem, tagName) -> dict:
        for e in elem:
            if e['tag_name'] == tagName:
                return e
    
    def getExcludes(self, selector, element):
        selector_paths = self.getSelectorPath(selector)
        if "content_tag" in selector_paths[-1]:
            for v in selector_paths[-1]['content_tag']:
                if v['tag_name'] == element:
                    elem = v
        if 'exclude' in elem:
            return elem['exclude']
        return None
    
    def getReplaces(self, selector, element):
        selector_paths = self.getSelectorPath(selector)
        if "content_tag" in selector_paths[-1]:
            for v in selector_paths[-1]['content_tag']:
                if v['tag_name'] == element:
                    elem = v
        if 'replace' in elem:
            return elem['replace']

#ISSUE: Problem with tag name. Current system, it doesn't make sense to return list when searching selector_path
#but we need it when we check the content tag. Look when home. Priority number 1.
    def getTagName(self, elem) -> [str]:
        tags = []
        #if 'tag_name' in elem:
        #    tags.append(elem['tag_name'])
        #else: tags.append(None)
        for t in elem:
            if 'tag_name' in t:
                tags.append(t['tag_name'])
            else:
                tags.append(None)
        return tags

    def getAttribute(self, elem) -> [str]:
        attributes = []
        #if 'attribute' in elem:
        #    attributes.append(elem['attribute'])
        #else: attributes.append(None)
        for t in elem:
            if 'attribute' in t:
                attributes.append(t['attribute'])
            else:
                attributes.append(None)        
        return attributes

    def getAttributeValue(self, elem) -> [str]:
        attribVal = []
        #if 'attributeValue' in elem:
        #    attribVal.append(elem['attributeValue'])
        #else: attribVal.append(None)
        for t in elem:
            if 'attributevalue' in t:
                attribVal.append(t['attributevalue'])
            else:
                attribVal.append(None)        
        return attribVal

    def getIsRecursive(self, elem) -> [bool]:
        rec = []
        #if 'recursive' in elem:
        #    rec.append(elem['recursive'])
        #else: rec.append(None)
        for t in elem:
            if 'recursive' in t:
                rec.append(t['recursive'])
        
        return rec

    def getIsTagOnly(self, elem) -> [bool]:
        rec = []
        #if 'recursive' in elem:
        #    rec.append(elem['recursive'])
        #else: rec.append(None)
        for t in elem:
            if 'tag_only' in t:
                rec.append(t['tag_only'])
        
        return rec