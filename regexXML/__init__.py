import re

def tag_regex(tag):
    '''
    Return a regular expression object for parsing XML by a given tag name.
    If elements with a same tag name exist on different levels,
    innermost elements will be parsed.
    '''

    return re.compile(
        r"<%s(?:\s*|\s+(?P<attr>[^><\/]*?))(?:>(?P<inner>(?:(?!<%s[>\s]).)*?)</%s>|\/>)" % (tag, tag, tag),
        re.DOTALL
    )

