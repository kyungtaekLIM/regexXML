import re
from collections import OrderedDict

attr_regex = re.compile(r"([\w\:]+?)\s*=\s*(\"[^\"\'<>]+?\"|\'[^<>\']+?\')")

def parse_attr(attr_str):
    attr = OrderedDict()
    if not attr_str:
        return attr

    for hit in attr_regex.finditer(attr_str):
        value = hit.group(2)
        if (value[0] == "\"" and value[-1] == "\"") or (value[0] == "\'" and value[-1] == "\'"):
            attr[hit.group(1)] = value[1:-1]
        else:
            attr[hit.group(1)] = value
    return attr

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

    def finditer(self, fileobj, batch_len=5000):
        xml = ""

        i = 0
        for line in fileobj:
            i += 1
            xml += line
            if i % batch_len:
                continue

            matches = [m for m in self.finditer_str(xml)]
            if matches:
                xml = xml[matches[-1].end():]  
                for m in matches:
                    yield m
        
        for m in self.finditer_str(xml):
            yield m


    def finditer_str(self, string):
        for g in self.tag_regex.finditer(string):
            yield g
    
    def search(self, iterable):
        return self.finditer(iterable)

    def search_str(self, string):
        return self.tag_regex.search(string)



