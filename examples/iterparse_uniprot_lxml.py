import os
from lxml import etree

filename = "uniprot_sprot.xml"

if not os.path.isfile(filename):
    err_tmpl = "%s was not found. Download ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz"
    raise IOError(err_tmpl % filename)

i = 0
for event, entry in etree.iterparse(filename, events=("end",), tag="entry"):
    for gene in entry.findall(".//gene"):
        name = gene.findall(".//name")
        if name:
            i += 1 
    entry.clear()

print("# of gene names: %s" % i)
