from lxml import etree

root = etree.fromstring(open("pubmed1.xml").read())
i = 0
for AuthorList in root.findall(".//AuthorList"):
    print("New author list")
    for Author in AuthorList.findall(".//Author"):
        LastName = Author.find(".//LastName")
        if LastName.text:
            print("%s: %s" % (LastName.text, Author.get("ValidYN")))
            i += 1
print(i)
