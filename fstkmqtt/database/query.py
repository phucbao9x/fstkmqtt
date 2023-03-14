class query:
    def CTB(fmt, tbn, *cols): 
        "get the create table query"
        ...
    def ITB(fmt, tbn, **pair): 
        "get the insert table query"
        ...
    def DTB(fmt, tbn, where) : 
        "get the delete table query"
        ...
    def UTB(fmt, tbn, **options) : 
        "get the update table query"
        ...
    def STB(fmt, tbn, *cols, **options) : 
        "get the select table query"
        ...
    def CDB(fmt, dbn) : 
        "get the select database query"
        return fmt%dbn