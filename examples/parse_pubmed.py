from regexXML import parse_attr, Tag

AuthorList_re = Tag("AuthorList")
LastName_re = Tag("LastName")
Author_re = Tag("Author")

i = 0
for AuthorList in AuthorList_re.finditer_str(open("pubmed1.xml").read()):
    print("New author list")
    for Author in Author_re.finditer_str(AuthorList.group()):
        LastName = LastName_re.search_str(Author.group("inner"))
        if LastName:
            print("%s: %s" % (LastName.group("inner"), parse_attr(Author.group("attr")).get("ValidYN")))
            i += 1
print(i)
