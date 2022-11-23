from .query import query
from ..supported.detecttype import istype
from .. import exceptions

class query(query):
    def CTB(fmt, tbn, *cols):
        return fmt%(tbn, ','.join(cols))
    
    def CDB(fmt, dbn):
        return fmt%dbn
    
    def ITB(fmt, tbn, **pair):
        tmp_cols = ','.join(list(pair.keys()))
        tmp_vals = ','.join([f'\'{i}\'' if istype(i, str) else str(i) for i in  list(pair.values())])
        return fmt%(tbn, tmp_cols, tmp_vals)

    def UTB(fmt, tbn, **options):
        where = options.pop('where', "")
        if where: where = f'where {where}'
        pair = options.pop('pair', None)
        if not pair: raise exceptions.MissingDataException('Pair')
        tmp_set = []
        for i in pair: tmp_set.append(f'{i}={pair[i]}')
        tmp_set = ','.join(tmp_set)
        return fmt%(tbn, tmp_set, where)

    def STB(fmt, tbn, *col,**options):
        where = options.pop('where', "")
        if where: where = f'where {where}'
        col = ','.join(col) if col else '*'
        return fmt%(tbn, col, where)
    
    def DTB(fmt, tbn, where):
        return fmt%(tbn, where)