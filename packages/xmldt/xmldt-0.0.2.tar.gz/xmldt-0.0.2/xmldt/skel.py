import sys

from xmldt import XMLDT
import argparse
import re


def build_skel(filename, name="DTSkel"):
    data = Skel(filename=filename)
    code = [f"""from xmldt import XMLDT
import sys


class {name} (XMLDT):

    def __default__(self, element):
          return f"[tag: {{element.tag}}, contents: {{element.contents}}]"
"""]
    for tag in data:
        method = re.sub("[.]", "_", tag)
        attr_count = str.join(" ", [f"{a}: {data[tag][a]}" for a in data[tag].keys() if a != ":count"])
        if method != tag:
            code.append(f"""    # @XMLDT.tag("{tag}")""")
        code.append(f"""    # def {method}(self, e): return e.tag # {data[tag][":count"]} occs   {attr_count}\n\n""")
    code.append(f"""
    
file = sys.argv[1]
dt = {name}()
print(dt(filename=file))\n""")
    return "\n".join(code)


def build_skel_jj(filename, name="proc"):
    #skel = Skeljj(filename=filename) --->FIXME: dá None

    ### claro que sim. o __default__ nao tme return
    ### ver a minha solucao abaixo

    skel = Skeljj()
    skel(filename=filename)
    print(
f"""#!/usr/bin/python3
from xmldt import XMLDT
import sys
class {name} (XMLDT):
    pass

    # def __default__(self, ele): 
    #     return f"[tag: {{ele.tag}}, cont: {{ele.contents}}]"
""")
    for tag in skel.order:
        v=skel.data[tag]
        attrs = str.join(" ", [f"{a}: {v[a]}" for a in v.keys()-{":count"}])
        print( "    #def","   "*(len(skel.ans[tag])-1),
            f"{tag}(self, ele): pass # {v[':count']} {attrs}" )
    print()
    print("file = sys.argv[1]")
    print(f"print({name}(filename=file))")


class Skeljj (XMLDT):

    data={}
    ans={}
    order=[]

    def __default__(self, ele):
        if ele.tag not in self.data:
            p = self.ans[ele.tag]=[a.tag for a in self.path]
            for tag in p+[ele.tag]:
                if tag in self.order: continue 
                self.order.append(tag)
            self.data[ele.tag] = {":count": 0}
        self.data[ele.tag][":count"] += 1
        for key in ele.attrs.keys():
            if key not in self.data[ele.tag]:
                self.data[ele.tag][key] = 0
            self.data[ele.tag][key] += 1


class Skel (XMLDT):

    data = {}

    def __default__(self, element):
        if element.tag not in self.data:
            self.data[element.tag] = {":count": 0}
        self.data[element.tag][":count"] += 1
        for key in element.attrs.keys():
            if key not in self.data[element.tag]:
                self.data[element.tag][key] = 0
            self.data[element.tag][key] += 1

    def __end__(self, _):
        return self.data


def main():
    arg_parser = argparse.ArgumentParser()
    skel = arg_parser.add_argument_group()
    skel.add_argument("-s", "--skel", help="Creates basic skeleton file", action="store_true")
    skel.add_argument("filename", type=str, help="the XML file to use as model")
    args = arg_parser.parse_args()

    if args.skel:
        print(build_skel(args.filename))
    else:
        build_skel_jj(args.filename)

