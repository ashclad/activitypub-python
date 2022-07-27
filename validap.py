from validators import url as urlvalidate

def createValidator(vfunc):
    def subfunc(*args):
        if len(args) > 3 or len(args) == 0:
            raise Exception()

        if len(args) == 1:
            return vfunc(args[0])

        if len(args) <= 3:
            if vfunc(args[0]):
                if callable(args[1]):
                    return args[1]()
                else:
                    return args[1]
            else:
                if callable(args[2]):
                    return args[2]()
                else:
                    return args[2]

    return subfunc

@createValidator
def chkcontentMapAttr(data):
    if isinstance(data, dict):
        for item in data:
            if not validlang(item):
                return False
            else:
                continue
    else:
        return False

@createValidator
def chkidAttr(data):
    if isinstance(data, str):
        if urlvalidate(data):
            return True
        else:
            return False
    elif isinstance(data, int):
        return True
    else:
        return False