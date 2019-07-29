#!/usr/bin/env python3
import os
import re
import argparse
import sys

def class_name(name):
    s = name.capitalize()
    regex = re.findall("_.", name)
    for a in regex:
        s = s.replace(a, a[1].upper())
    return s



def create_project(name=None):
    if not name:
        name = sys.argv[1]
    os.makedirs(name, exist_ok=True)
    os.chdir(name)
    with open(name+".py", 'w') as w:
        s = """\
from heorot.heorot import Hall\n
class {}(Hall):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
if __name__ == '__main__':
    n = {}()
    n.run()""".format(class_name(name), class_name(name))
        w.write(s)
    os.makedirs("static", exist_ok=True)
    os.makedirs("template", exist_ok=True)
    os.chdir("..")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", action="store", help="project name")
    args = parser.parse_args()
    create_project(name=args.name)
    # print(class_name(args.name))
