import os
from lxml import etree

filename = "uniprot_sprot.xml"

if not os.path.isfile(filename):
    raise IOError(
        "%s was not found. Download a gz file from ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz and decompress it" %
        filename
    )

i = 0
for event, entry in etree.iterparse(filename, events=("end",), tag="entry"):
    for gene in entry.findall(".//gene"):
        name = gene.findall(".//name")
        if name:
            i += 1 
    entry.clear()

print("# of gene names: %s" % i)
