from regexXML import Tag

entry_re = Tag("entry")
gene_re = Tag("gene")
name_re = Tag("name")

i = 0
for entry in entry_re.finditer_from_file(open("uniprot-all.xml")):
    for gene in gene_re.finditer(entry.group()):
        name = name_re.search(gene.group("inner"))
        if name:
            i += 1
print(i)
