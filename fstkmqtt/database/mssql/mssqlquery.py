from .._query import query as q

class query:
    def CDB(dbn : str, end: str= ';'):
        return q.CDB(f'CREATE DATABASE %s', dbn).strip() + end
    
    def CTB(tbn : str, *col ,end: str= ';'):
        return q.CTB('CREATE TABLE %s (%s)', tbn, col).strip() + end
    
    def ITB(tbn: str, end: str = ';', **pair):
        return q.ITB('INSERT INTO %s (%s) VALUES(%s)', tbn, pair).strip() + end
    
    def UTB(tbn, end: str = ';', **options):
        return q.UTB('UPDATE %s SET %s %s',tbn, options).strip() + end
    
    def STB(tbn, *col, end:str = ';',**options):
        return q.STB('SELECT %s FROM %s %s', tbn, *col, **options).strip() + end
    
    def DTB(tbn: str, where : str, end: str = ';'):
        return q.DTB('DELETE TABLE %s %s', tbn, where).strip + end