from xmldt import XMLDT
import argparse


def build_skel(filename, name="DTSkel"):
    skel = Skel()
    skel(filename=filename)
    print("""from xmldt import XMLDT""")
    print("""import sys""")
    print()
    print()
    print(f"""class {name} (XMLDT):""")
    print()
    print("    def __default__(self, element):")
    print("""         return f"[tag: {element.tag}, contents: {element.contents}]" """)
    print()
    for tag in skel.data:
        attr_count = str.join(" ", [f"{a}: {skel.data[tag][a]}" for a in skel.data[tag].keys() if a != ":count"])
        print(f"""    # def {tag}(self, element):  # {skel.data[tag][":count"]} occurrences   {attr_count}""")
        print(f"""    #    return element.tag""")
        print()
    print()
    print()
    print("""file = sys.argv[1]""")
    print(f"""dt = {name}()""")
    print("""print(dt(filename=file))""")


class Skel (XMLDT):

    def __init__(self):
        super().__init__()
        self.data = dict()

    def __join__(self, child):
        return None

    def __default__(self, element):
        if element.tag not in self.data:
            self.data[element.tag] = {":count": 0}
        self.data[element.tag][":count"] += 1
        for key in element.attrs.keys():
            if key not in self.data[element.tag]:
                self.data[element.tag][key] = 0
            self.data[element.tag][key] += 1


def main():
    arg_parser = argparse.ArgumentParser()
    skel = arg_parser.add_argument_group()
    skel.add_argument("-s", "--skel", help="Creates basic skeleton file", action="store_true")
    skel.add_argument("filename", type=str, help="the XML file to use as model")
    args = arg_parser.parse_args()

    if args.skel:
        build_skel(args.filename)


