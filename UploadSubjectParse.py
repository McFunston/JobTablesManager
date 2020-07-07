import sys
import re
def SubjectParse(name):
    name = name.replace('-','_')
    name = name.replace('(','_')
    name = name.replace(' ','_')
    name = name.replace('[','_')
    name = name.replace(']','_')
    splitName = name.split('_')
    for fragment in splitName:
        if fragment.isnumeric() and len(fragment) > 1:
            return fragment

#print(SubjectParse("Best Version Media File Upload - File (1825_Airport_Apr2020_PRESS.pdf) Waiting for Pickup"))

if __name__ == "__main__":
    print(SubjectParse(sys.argv[1]))
