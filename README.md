# regexXML

`regexXML` is a pure Python library for fast and memory-efficient XML parsing.

Python XML libaries such as `lxml` are extremely memory-demanding. `regexXML` simply uses regular expressions to extract elements from XML by a tag name, and to parse attributes of those elements. By doing so, `regexXML` is faster and consumes much less memory than `lxml`. `regexXML` allows you to parse gigabytes (or even terabytes) of XML files without a luxurious computer.

## Installation

`regexXML` runs under Python 2 and 3.

You can install using pip.

```
pip install git+https://github.com/kyungtaekLIM/regexXML.git
```

## Usage

To use regexXML, first import Attr and Tag classes.

```python
from regexXML import Attr, Tag
```

Make regex (regular expression) objects of tag names you want to parse using `Tag`.

```python
gene_re = Tag("gene")
name_re = Tag("name")
entry_re = Tag("entry")
```

To get a single tag match from an XML string, use `search`, which will give you a match object. Once you get a match object, group() will give you the matched string. Its attribute and inner-XML can be extracted by group("attr") and group("inner"), respectively.

```python
gene = gene_re.search(xml_string)
tag_string = gene.group()
attribute_string = gene.group("attr")
inner_xml_string = gene.group("inner")
```

To iterate over all matches, use `finditer`. `Attr` parses the attribute string and returns an OrderedDict object.

```python
for name in name_re.finditer(gene.group("inner")):
    tag_string = name.group()
    attribute_string = name.group("attr")
    inner_xml_string = name.group("inner")
    
    attribute_dict = Attr(attribute_string)
```

If your XML file is huge, it is a bad idea to read the whole file at once. To prevent your computer from being low on memory, use `finditer_from_file` that reads chunks of a file to parse tags iteratively.

```python
with open(filename, "r") as f:
    for entry in entry_re.finditer_from_file(f):
        tag_string = name.group()
        attribute_string = name.group("attr")
        inner_xml_string = name.group("inner")
    
        attribute_dict = Attr(attribute_string)
```


## Examples

### 1) Parsing an XML string

Here is an example of parsing an XML document from Uniprot database (http://uniprot.org).

```python
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
for name in name_re.finditer(gene.group("inner")):
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
```

### 2) Parsing a huge XML file iteratively.

An example of parsing a huge Uniport XML file (5.9G) downloaded from  ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz in a memory-efficient manner.

```python
from regexXML import Tag

entry_re = Tag("entry")
gene_re = Tag("gene")
name_re = Tag("name")

filename = "uniprot_sprot.xml"

with open(filename, "r") as f:
    i = 0
    for entry in entry_re.finditer_from_file(f):
        for gene in gene_re.finditer(entry.group("inner")):
            name = name_re.search(gene.group("inner"))
            if name:
                i += 1

    print("# of gene names: %s" % i)
```

I compared CPU time and maximum memory usage required to run this script with [the `lxml` equivalent](https://github.com/kyungtaekLIM/regexXML/blob/master/examples/iterparse_uniprot_lxml.py). `regexXML` is superior to `lxml`.

| Library   | CPU Time (s) | Max Memory |
| ----------| ------------ | ---------- |
| regexXML  | 150          | 139M       |
| lxml      | 191          | 239M       |



### 3) parsing a gzipped XML file iteratively.

If you want to parse the above XML file without decompressing it, just open the file using `gzip` library.

```python
import gzip
from regexXML import Tag

entry_re = Tag("entry")
gene_re = Tag("gene")
name_re = Tag("name")

filename = "uniprot_sprot.xml.gz"

with gzip.open(filename, "r") as f:
    i = 0
    for entry in entry_re.finditer_from_file(f):
        for gene in gene_re.finditer(entry.group("inner")):
            name = name_re.search(gene.group("inner"))
            if name:
                i += 1

    print("# of gene names: %s" % i)
```

I also compared CPU time and maximum memory usage with [the `lxml` equivalent](https://github.com/kyungtaekLIM/regexXML/blob/master/examples/iterparse_uniprot_lxml_gzip.py). Again, `regexXML` is superior to `lxml`.


| Library   | CPU Time (s) | Max Memory |
| ----------| ------------ | ---------- |
| regexXML  | 167          | 150M       |
| lxml      | 214          | 243M       |




