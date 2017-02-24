import re
from collections import OrderedDict


class Attr(OrderedDict):

    attr_regex = re.compile(r"([\w\:]+?)\s*=\s*(\"[^\"\'<>]+?\"|\'[^<>\']+?\')")
    
    def __init__(self, attr_str):
        for hit in self.attr_regex.finditer(attr_str):
            value = hit.group(2)
            if (value[0] == "\"" and value[-1] == "\"") or (value[0] == "\'" and value[-1] == "\'"):
                self[hit.group(1)] = value[1:-1]
            else:
                self[hit.group(1)] = value


class Tag:

    def __init__(self, tag):
        self.tag = tag
        self.tag_regex = self.compile_tag_regex(tag)   

    @classmethod
    def compile_tag_regex(cls, tag):
        '''
        Return a regular expression object for parsing XML by a given tag name.
        If elements with a same tag name exist on different levels,
        innermost elements will be parsed.
        '''
        
        return re.compile(
            r"<%s(?: *| +(?P<attr>[^><]*?))(?:>(?P<inner>(?!<%s )(?!<%s>).*?)</%s>|\/>)" % (tag, tag, tag, tag),
            re.DOTALL
        )

    def finditer_from_file(self, fileobj, chunk_size=300000):
        xml = ""

        chunk = fileobj.read(chunk_size)
        while chunk:
            xml += chunk

            end_index = 0
            for m in self.finditer(xml):
                end_index = m.end()
                yield m
            
            if end_index:
                xml = xml[end_index:]

            chunk = fileobj.read(chunk_size)
        
        for m in self.finditer(xml):
            yield m

    def finditer(self, string):
        for g in self.tag_regex.finditer(string):
            yield g
    
    def search_from_file(self, fileobj, chunk_size=300000):
        for m in self.finditer_from_file(fileobj, chunk_size=300000):
            return m

    def search(self, string):
        return self.tag_regex.search(string)



