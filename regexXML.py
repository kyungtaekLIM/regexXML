import re
from collections import OrderedDict

__version__ = "0.4.6"


class Attr(OrderedDict):

    pattern = re.compile(r"([\w\-\.:]+?)\s*=\s*(\"[^\"&<]+?\"|\'[^\'&<]+?\')")

    def __init__(self, attr_str):
        super(Attr, self).__init__()
        if attr_str:
            for hit in self.pattern.finditer(attr_str):
                key, value = hit.groups()
                self[key] = value[1:-1]


class Tag:

    def __init__(self, tag):
        self.tag = tag
        self.pattern = self.get_pattern(tag)   

    @classmethod
    def get_pattern(cls, tag):
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
            for m in self.pattern.finditer(xml):
                end_index = m.end()
                yield m
            
            if end_index:
                xml = xml[end_index:]

            chunk = fileobj.read(chunk_size)

    def finditer(self, string):
        for g in self.pattern.finditer(string):
            yield g
    
    def search_from_file(self, fileobj, chunk_size=300000):
        for m in self.finditer_from_file(fileobj, chunk_size=300000):
            return m

    def search(self, string):
        return self.pattern.search(string)



