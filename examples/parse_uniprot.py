from regexXML import Attr, Tag

uniprot_xml = """
<?xml version="1.0" ?>
<uniprot schemaLocation="http://uniprot.org/uniprot http://www.uniprot.org/support/docs/uniprot.xsd">
 <entry created="2009-03-24" dataset="Swiss-Prot" modified="2017-03-15" version="59">
  <accession>B0TGS9</accession>
  <name>FMT_HELMI</name>
  <protein>
   <recommendedName>
    <fullName evidence="1">Methionyl-tRNA formyltransferase</fullName>
    <ecNumber evidence="1">2.1.2.9</ecNumber>
   </recommendedName>
  </protein>
  <gene>
   <name evidence="1" type="primary">fmt</name>
   <name type="ordered locus">Helmi_20650</name>
   <name type="ORF">HM1_2133</name>
  </gene>
  <organism>
   <name type="scientific">Heliobacterium modesticaldum (strain ATCC 51547 / Ice1)</name>
   <dbReference id="498761" type="NCBI Taxonomy"/>
   <lineage>
    <taxon>Bacteria</taxon>
    <taxon>Firmicutes</taxon>
    <taxon>Clostridia</taxon>
    <taxon>Clostridiales</taxon>
    <taxon>Heliobacteriaceae</taxon>
    <taxon>Heliobacterium</taxon>
   </lineage>
  </organism>
 </entry>
</uniprot>
"""

gene_re = Tag("gene")
name_re = Tag("name")

i = 0
gene = gene_re.search(uniprot_xml)

print("# print gene element")
print("%s\n" % gene.group())

print("# print inner-xml of gene element")
print("%s\n" % gene.group("inner"))

print("# print attribute string of gene element")
print("%s\n" % gene.group("attr"))

for name in name_re.finditer(uniprot_xml):
    print("# print name element")
    print("%s\n" % name.group())

    print("# print inner-xml of name element")
    print("%s\n" % name.group("inner"))

    print("# print attribute string of name element")
    print("%s\n" % name.group("attr"))
    
    attr = Attr(name.group("attr"))
    print("# print parsed attributes")

    for k, v in attr.items():
        print("key : %s\nvalue : %s\n" % (k, v))


