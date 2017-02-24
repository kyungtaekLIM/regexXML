from regexXML import Attr, Tag

AuthorList_re = Tag("AuthorList")
LastName_re = Tag("LastName")
Author_re = Tag("Author")

i = 0
for AuthorList in AuthorList_re.finditer(open("pubmed1.xml").read()):
    print("New author list")
    for Author in Author_re.finditer(AuthorList.group()):
        LastName = LastName_re.search(Author.group("inner"))
        if LastName:
            print("%s: %s" % (LastName.group("inner"), Attr(Author.group("attr")).get("ValidYN")))
            i += 1
print(i)
