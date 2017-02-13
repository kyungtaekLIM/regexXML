import re
from collections import OrderedDict

attr_regex = re.compile(r"([\w\:]+?)\s*=\s*(?:\"([^\"'<>\/]+?)\"|\'([^<>\/']+?)\')")

def parse_attr(attr_str):
    attr = OrderedDict()
    if not attr_str:
        return attr

    for hit in attr_regex.finditer(attr_str):
        if hit.group(2):
            attr[hit.group(1)] = hit.group(2)
        elif hit.group(3):
            attr[hit.group(1)] = hit.group(3)
    return attr

def compile_tag_regex(tag):
    '''
    Return a regular expression object for parsing XML by a given tag name.
    If elements with a same tag name exist on different levels,
    innermost elements will be parsed.
    '''

    return re.compile(
        r"<%s(?:\s*|\s+(?P<attr>[^><\/]*?))(?:>(?P<inner>(?:(?!<%s[>\s]).)*?)</%s>|\/>)" % (tag, tag, tag),
        re.DOTALL
    )

