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
    if len(candidates) > 2:
        return candidates[1]
    elif len(candidates) >= 1:
        return candidates[0]
    else:
        return 0

# print(NameParspython3 e("75_Kris_Locke_2933_NeighboursOfFairfield_Jul2020_p1-16_15"))

if __name__ == "__main__":
    print(NameParse(sys.argv[1]))
