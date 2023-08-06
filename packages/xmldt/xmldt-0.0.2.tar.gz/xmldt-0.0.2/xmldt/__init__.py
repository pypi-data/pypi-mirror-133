"""
  python module to Down Translate XML

Synopsis
========

# Description

"""
from lxml.etree import XMLParser, parse, fromstring
from xmldt.element import Element
import sys

__version__ = "0.0.2"
__docformat__ = 'markdown'


class XMLDT:

    @classmethod
    def tag(cls, name):
        def decorator(func):
            def tmp(*args, **kwargs):
                return func(*args, **kwargs)

            tmp.has_alias = name
            return tmp
        return decorator

    @classmethod
    def datatype(cls, name):
        if name not in ("list", "string", "list_of_dicts", "the_child", "last_child", "dict", "zero"):
            raise Exception(f"Decorator type with invalid value {name}")

        def decorator(func):
            def _decorator(*args, **kwargs):
                return func(*args, **kwargs)

            _decorator.has_type = name
        return decorator

    def __init__(self, strip=False, empty=False):
        self._parser = XMLParser()
        self._path = []
        self._strip = strip
        self._empty = empty

        self._alias = {
            method.has_alias: method for method in {
                getattr(self, name) for name in dir(self)
                if callable(getattr(self, name)) and hasattr(getattr(self, name), "has_alias")}}

        self._types = {
            method: method.has_type for method in {
                getattr(self, name) for name in dir(self)
                if callable(getattr(self, name)) and hasattr(getattr(self, name), "has_type")}}

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
        return self.__end__(self.__recurse_node__(self.root))

    def __pcdata__(self, text):
        """Method called to process text nodes. If you override it, call its superclass method to
           guarantee empty and strip options to be honored"""
        if not self._empty and str.isspace(text):
            return None
        if self._strip:
            text = text.strip()
        return text

    def __default__(self, element):
        """Default handler for XML elements, when no specific handler is defined"""
        return element.xml

    def __end__(self, result):
        """Handler called after DT process, so it can be used for final processing tasks"""
        return result

    def __recurse_node__(self, child):
        # copy attributes, so we can store whatever object we want
        self._path.append(Element(child.tag, {**child.attrib}, None, self))

        if child.tag in self._alias:
            tag_handler = self._alias[child.tag]
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
        return str.join("", [ele for ele in child if ele] )

    @property
    def path(self):
        return self._path

