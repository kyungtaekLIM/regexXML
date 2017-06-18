import os
import gzip
from regexXML import Tag

entry_re = Tag("entry")
gene_re = Tag("gene")
name_re = Tag("name")

filename = "uniprot_sprot.xml.gz"

if not os.path.isfile(filename):
    err_tmpl = "%s was not found. Download ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz"
    raise IOError(err_tmpl % filename)

with gzip.open(filename, "r") as f:
    i = 0
    for entry in entry_re.finditer_from_file(f):
        for gene in gene_re.finditer(entry.group("inner")):
            name = name_re.search(gene.group("inner"))
            if name:
                i += 1

    print("# of gene names: %s" % i)
