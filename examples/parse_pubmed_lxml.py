from lxml import etree

root = etree.fromstring(open("pubmed1.xml").read())

AuthorList = root.find(".//AuthorList")
print("Author List")
for Author in AuthorList.findall(".//Author"):
    LastName = Author.find(".//LastName")
    ForeName = Author.find(".//ForeName")
    print("%s %s (ValidYN: %s)" % 
        (
            ForeName.text,
            LastName.text,
            # parse attributes of an Auther tag and
            # get the value of ValidYN
            Author.get("ValidYN")
        )
    )
