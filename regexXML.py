import re

#compile regex for parsing an XML tag
def xml_tag_pattern(tag):
    return re.compile(r'<%s[^>]*?(>.*?<\/%s>|\/>)' % (tag, tag), re.DOTALL)
