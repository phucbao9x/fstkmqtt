def istype(object, cast : type):
    return type(object) is cast

def anytype(object, castes : list[type]):
    return any([istype(object, cast) for cast in castes])