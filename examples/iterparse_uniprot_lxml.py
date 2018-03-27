import os
import gzip
from lxml import etree

filename = "uniprot_sprot.xml"

if not os.path.isfile(filename):
    err_tmpl = "%s was not found. Download ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz"
    raise IOError(err_tmpl % filename)

ns = "http://uniprot.org/uniprot"

with open(filename, "rb") as f:
    i = 0
    for event, entry in etree.iterparse(f, events=("end",), tag="{%s}entry" % ns):
        for gene in entry.findall(".//{%s}gene" % ns):
            for name in gene.findall(".//{%s}name" %ns):
                if name is not None and name.get("type") == "primary":
                    i += 1
        entry.clear()

    print("# of primary gene names: %s" % i)
