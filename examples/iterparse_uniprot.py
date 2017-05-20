import os
from regexXML import Tag

entry_re = Tag("entry")
gene_re = Tag("gene")
name_re = Tag("name")

filename = "uniprot_sprot.xml"

if not os.path.isfile(filename):
    raise IOError(
        "%s was not found. Download a gz file from ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz and decompress it" %
        filename
    )

i = 0
for entry in entry_re.finditer_from_file(open(filename)):
    for gene in gene_re.finditer(entry.group()):
        name = name_re.search(gene.group("inner"))
        if name:
            i += 1

print("# of gene names: %s" % i)
