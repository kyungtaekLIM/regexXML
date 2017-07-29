import re
from collections import OrderedDict

__version__ = "0.5.0"


class Attr(OrderedDict):

    pattern = re.compile(r"([\w\-\.:]+?)\s*=\s*(\"[^\"&<]+?\"|\'[^\'&<]+?\')")

    def __init__(self, attr_str):
        super(Attr, self).__init__()
        if attr_str:
            for hit in self.pattern.finditer(attr_str):
                key, value = hit.groups()
                self[key] = value[1:-1]


class Tag:

    def __init__(self, tag, nested=True):
        self.tag = tag
        self.pattern = self.get_pattern(tag, nested=nested) 

    @classmethod
    def get_pattern(cls, tag, nested=True):
        '''
        Return a regular expression object for parsing XML by a given tag name.
        If elements with a same tag exist on different levels, the innermost
        element will be parsed. If the tag does not form a nested structure,
        set nested=False for speed.
        '''
<<<<<<< HEAD

        if nested:
            return re.compile(
                r"<%s(?: *| +(?P<attr>[^&<]*))(?:>(?P<inner>(?:(?!<%s[ >]).)*?)</%s>|></%s>|\/>)" % (tag, tag, tag, tag),
                re.DOTALL
            )
        else:
           return re.compile(
                r"<%s(?: *| +(?P<attr>[^&<]*))(?:>(?P<inner>.*?)</%s>|\/>)" % (tag, tag),
                re.DOTALL
            )

    def finditer_from_file(self, fileobj, chunk_size=300000):

        xml = fileobj.read(chunk_size)

        while True:

            end_index = 0
            for m in self.pattern.finditer(xml):
                end_index = m.end()
                yield m
            
            chunk = fileobj.read(chunk_size)

            if chunk:
                if end_index:
                    xml = xml[end_index:] + chunk
                else:
                    xml += chunk
            else:
                break

    def finditer(self, string):
        for g in self.pattern.finditer(string):
            yield g
    
    def search_from_file(self, fileobj, chunk_size=300000):
        for m in self.finditer_from_file(fileobj, chunk_size=300000):
            return m

    def search(self, string):
        return self.pattern.search(string)



