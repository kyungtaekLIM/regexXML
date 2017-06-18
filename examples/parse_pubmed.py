from regexXML import Attr, Tag

# make Tag objects
AuthorList_re = Tag("AuthorList")
Author_re = Tag("Author")
LastName_re = Tag("LastName")
ForeName_re = Tag("ForeName")

# search the fisrt AuthorList tag
AuthorList = AuthorList_re.search(open("pubmed1.xml").read())

print("Author List")
# find Author tags
for Author in Author_re.finditer(AuthorList.group("inner")):
    # search LastName and ForeName tags
    Author_inner = Author.group("inner")
    LastName = LastName_re.search(Author_inner)
    ForeName = ForeName_re.search(Author_inner)
    print("%s %s (ValidYN: %s)" % 
        (
            ForeName.group("inner"),
            LastName.group("inner"),
            # parse attributes of an Auther tag and
            # get the value of ValidYN
            Attr(Author.group("attr")).get("ValidYN")
        )
    )
