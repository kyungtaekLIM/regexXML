from lxml import etree
i = 0
for event, entry in etree.iterparse("uniprot-all.xml", events=("end",), tag="entry"):
    for gene in entry.findall(".//gene"):
        name = gene.findall(".//name")
        if name:
            i += 1 
    entry.clear()
print(i)
