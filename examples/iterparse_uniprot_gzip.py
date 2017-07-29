import os
import gzip
from regexXML import Tag, Attr

entry_re = Tag("entry", nested=False)
gene_re = Tag("gene", nested=False)
name_re = Tag("name", nested=False)

filename = "uniprot_sprot.xml.gz"

if not os.path.isfile(filename):
    err_tmpl = "%s was not found. Download ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz"
    raise IOError(err_tmpl % filename)

with gzip.open(filename, "rt") as f:
    i = 0
    for entry in entry_re.finditer_from_file(f):
        for gene in gene_re.finditer(entry.group("inner")):
            for name in name_re.finditer(gene.group("inner")):
                if name:
                    name_attr = Attr(name.group("attr"))
                    if name_attr.get("type") == "ORF":
                        i += 1

    print("# of ORF gene names: %s" % i)
