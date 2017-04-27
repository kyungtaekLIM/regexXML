# regexXML

`regexXML` provides python functions for parsing XML.
One can extract elements from XML by a tag name, and parse attributes of those elements with `regexXML`.
As python XML libaries such as `lxml` are extremely memory-demanding,`regexXML` will help parse very very big XML files in a memory-efficient manner.
from regexXML import Attr, Tag

## Examples

Here is an example of parsing a simple XML from Uniprot database (http://uniprot.org) using regexXML.

<pre>python
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

# search "gene" tag that comes first.
gene = gene_re.search(uniprot_xml)

# get the whole XML of the gene element.
print("# print the first gene element")
print("%s\n" % gene.group())

# get inner-XML of the gene element.
print("# print inner-XML of the gene element")
print("%s\n" % gene.group("inner"))

# get the attribute string of the gene element.
# Return None, if it does not exist.
print("# print attribute string of the gene element")
print("%s\n" % gene.group("attr"))

# iterate over name elements in the gene element.
for name in name_re.finditer(gene.group()):
    print("# print a name element")
    print("%s\n" % name.group())

    print("# print inner-XML of the name element")
    print("%s\n" % name.group("inner"))

    print("# print the attribute string of the name element")
    print("%s\n" % name.group("attr"))
    
    # parse the attribute string into OrderedDict.
    attr = Attr(name.group("attr"))

    # get key-value pairs of the attribute.
    print("# print parsed attributes")
    for k, v in attr.items():
        print("key : %s\nvalue : %s\n" % (k, v))
</pre>
