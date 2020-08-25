import sys
import re
def NameParse(name):
    name = name.replace('-','_')
    name = name.replace(' ','_')
    splitName = name.split('_')
    candidates=list()
    for fragment in splitName:        
        if fragment.isnumeric() and len(fragment) > 1:
            candidates.append(fragment)
    if len(candidates) == 2:
        return candidates[1]
    elif len(candidates) == 1:
        return candidates[0]
    else:
        print("Name not Found")
        return 0


