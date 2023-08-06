
class Element:

    def __init__(self, tag, attributes, content, dt=None):
        self._tag = tag
        self._attributes = attributes
        self._content = content
        self._dt = dt

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    @property
    def q(self):
        return self._tag

    @q.setter
    def q(self, value):
        self._tag = value

    @property
    def contents(self):
        return self._content

    @contents.setter
    def contents(self, value):
        self._content = value

    @property
    def c(self):
        return self._content

    @c.setter
    def c(self, value):
        self._content = value

    @property
    def attrs(self):
        return self._attributes

    @property
    def v(self):
        return self._attributes

    def __getitem__(self, item):
        return self._attributes[item] if item in self._attributes else None

    def __setitem__(self, key, value):
        self._attributes[key] = value

    def toxml(self):
        ats = str.join("", [f' {a}="{b}"' for a,b in self._attributes.items()])
        tag = f"<{self.tag}{ats}"
        if self.contents is not None and len(self.contents) > 0:
            tag += f">{self._content}</{self.tag}>"
        else:
            tag += "/>"
        return tag

    @property
    def xml(self):
        return self.toxml()

    @property
    def father(self):
        return None if self._dt is None or len(self._dt.path) < 2 else self._dt.path[-2]

    @property
    def gfather(self):
        return None if self._dt is None or len(self._dt.path) < 3 else self._dt.path[-3]
