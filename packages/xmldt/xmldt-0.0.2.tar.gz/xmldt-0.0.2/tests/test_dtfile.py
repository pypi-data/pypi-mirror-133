import pytest

from xmldt import XMLDT


def test_simple_file():
    class T1 (XMLDT):
        pass

    t1 = T1(strip=True, empty=False)
    assert t1(filename="tests/test1.xml") == """<root>text<body>more text</body>text</root>"""


def test_raise():
    class T1 (XMLDT):
        pass

    t1 = T1()
    with pytest.raises(Exception, match="DT called without arguments"):
        t1()


