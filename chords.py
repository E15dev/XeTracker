# these are chord definitions
# TODO: CHANGE TO DICT SO IT WILL BE EASIER TO MATCH
MAJ = [0, 4, 7]
MIN = [0, 3, 7]
POW = [0, 7, 12]

class chrdnf(Exception):
    """when wrong chord name"""
    pass

class nmp(Exception):
    "when you need more patterns"
    pass

def mch(nm: str):
    match nm.lower():
        case "maj":
            return MAJ
        case "min":
            return MIN
        case "pow":
            return POW
    raise chrdnf
