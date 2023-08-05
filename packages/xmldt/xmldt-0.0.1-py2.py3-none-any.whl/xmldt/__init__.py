"""
  python module to Down Translate XML

Synopsis
========

# Description

"""
from lxml.etree import XMLParser, parse, fromstring
from xmldt.element import Element

__version__ = "0.0.1"
__docformat__ = 'markdown'

#
# def sequence(func):
#     def _decorator(*args, **kwargs):
#         func(*args, **kwargs)
#     _decorator.is_sequence = True
#     return _decorator


class XMLDT:

    @classmethod
    def TAG(cls, name):
        def decorator(func):
            def tmp(*args, **kwargs):
                return func(*args, **kwargs)

            tmp._has_alias = name
            return tmp
        return decorator

    def __init__(self, strip=False, empty=False):
        self._parser = XMLParser()
        self._path = []
        self._strip = strip
        self._empty = empty

        self._alias = {
            method._has_alias : method for method in {
                getattr(self, name) for name in dir(self)
                if callable(getattr(self, name)) and hasattr(getattr(self, name), "_has_alias")}}

       # sequences = {name for name in dir(self) if callable(getattr(self, name)) and hasattr(getattr(self, name), "is_sequence")}
       # print(sequences, file=sys.stderr)

    def __new__(cls, xml=None, filename=None, strip=False, empty=False):
        ## nao gosto, mas funciona
        self = super(XMLDT, cls).__new__(cls)
        self.__init__(strip, empty)

        if filename is not None or xml is not None:
            return self(xml, filename)
        else:
            return self

    def __call__(self, xml=None, filename=None):
        if filename is not None:
            self.tree = parse(filename, parser=self._parser)
            self.root = self.tree.getroot()
        elif xml is not None:
            self.tree = fromstring(xml, parser=self._parser)
            self.root = self.tree
        else:
            raise Exception("DT called without arguments")
        return self.__recurse_node__(self.root)

    def __pcdata__(self, text):
        if not self._empty and str.isspace(text):
            return None
        if self._strip:
            text = text.strip()
        return text

    def __default__(self, element):
        return element.xml

    def __recurse_node__(self, child):
        # copy attributes, so we can store whatever object we want
        self._path.append(Element(child.tag, {**child.attrib}, None, self))

        if child.tag in self._alias:
            tag_handler = self._alias[child.tag] #  getattr(self, self._alias[child.tag], self.__default__)
        else:
            tag_handler = getattr(self, child.tag, self.__default__)
            if not callable(tag_handler):
                tag_handler = self.__default__

        self._path[-1].contents = self.__dt__(child)
        result = tag_handler(self._path[-1])
        self._path.pop()

        return result

    def __dt__(self, tree):
        results = []
        if tree.text:
            r = self.__pcdata__(tree.text)
            if r:
                results = [r]
        for child in tree:
            results.append(self.__recurse_node__(child))
            if child.tail:
                r = self.__pcdata__(child.tail)
                if r:
                    results.append(r)
        return self.__join__(results)

    def __join__(self, child):  # would prefer __reduce__, but that is builtin for python
        return str.join("", child)

    @property
    def path(self):
        return self._path

