import os
import gzip
from lxml import etree

filename = "uniprot_sprot.xml.gz"

if not os.path.isfile(filename):
    err_tmpl = "%s was not found. Download ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz"
    raise IOError(err_tmpl % filename)

with gzip.open(filename) as f:
    i = 0
    for event, entry in etree.iterparse(f, events=("end",), tag="entry"):
        for gene in entry.findall(".//gene"):
            for name in gene.findall(".//name"):
                if name is not None and name.get("type") == "ORF":
                    i += 1
        entry.clear()

    print("# of ORF gene names: %s" % i)
