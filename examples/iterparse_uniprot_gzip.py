import os
import sys
import gzip
from regexXML import Tag, Attr

entry_re = Tag("entry", nested=False)
gene_re = Tag("gene", nested=False)
name_re = Tag("name", nested=False)

filename = "uniprot_sprot.xml.gz"

if not os.path.isfile(filename):
    err_tmpl = "%s was not found. Download ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz"
    raise IOError(err_tmpl % filename)

if sys.version_info[0] == 3:
    mode = "rt"
else:
    mode = "r"

with gzip.open(filename, mode) as f:
    i = 0
    j = 0
    for entry in entry_re.finditer_from_file(f):
        for gene in gene_re.finditer(entry.group("inner")):
            for name in name_re.finditer(gene.group("inner")):
                name_attr = Attr(name.group("attr"))
                if name_attr.get("type") == "primary":
                    i += 1
        j += 1
    
    print("# of primary gene names: %s" % i)
