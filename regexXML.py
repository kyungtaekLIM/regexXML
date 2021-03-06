import re
from collections import OrderedDict

__version__ = "0.7.0"


class Attr(OrderedDict):

    pattern = re.compile(r"([\w\-\.:]+?)\s*=\s*(\"[^\"&<]+?\"|\'[^\'&<]+?\')")

    def __init__(self, attr_str):
        super(Attr, self).__init__()
        if attr_str:
            for hit in self.pattern.finditer(attr_str):
                key, value = hit.groups()
                self[key] = value[1:-1]


class Tag:

    def __init__(self, tag, nested=False, attr_only=False, attr_pattern=None):
        '''
        Tag object.

        Parameters
        ----------

        tag : string
            tag name
        nested : boolean
            True if elements with a same tag exist on different levels. Then the innermost
            element will be parsed. False if not nested.
        attr_only : boolean
            True when to parse attributes only.
        attr_pattern : regex pattern
            If not None, tag elements with attributes including this regex pattern will be
            parsed.
        '''

        self.tag = tag
        self.pattern = self.get_pattern(
            tag,
            nested=nested,
            attr_only=attr_only,
            attr_pattern=attr_pattern
        )

    @classmethod
    def get_pattern(cls, tag, nested=False, attr_only=False, attr_pattern=None):
        """
        Return a regular expression object for parsing XML by a given tag name.
        See Tag class for parameters.

        Parameters
        ----------

        tag : string
            tag name
        nested : boolean
            True if elements with a same tag exist on different levels. Then the innermost
            element will be parsed. False if not nested.
        attr_only : boolean
            True when to parse attributes only.
        attr_pattern : regex pattern
            If not None, tag elements with attributes including this regex pattern will be
            parsed.


        Returns
        -------
        o : regex object
            A compiled Python regex object
            
        """

        if attr_pattern:
            re_string = r"<{0}\s+(?P<attr>%s[^&<]*|[^&<]+\s+%s[^&<]*)" % (attr_pattern, attr_pattern)
        else:
            re_string = r"<{0}(?:\s*|\s+(?P<attr>[^&<]*))"

        if attr_only:
            re_string += r"(>|/>)"

            return re.compile(
                re_string.format(tag),
                re.DOTALL
            )

        if nested:
            re_string += r"(?:>(?P<inner>(?:(?!<{0}[ >]).)*?)</{0}>|></{0}>|\/>)"
        else:
            re_string += r"(?:>(?P<inner>.*?)</{0}>|/>)"

        return re.compile(
            re_string.format(tag),
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
        for m in self.finditer_from_file(fileobj, chunk_size=chunk_size):
            return m

    def search(self, string):
        return self.pattern.search(string)
