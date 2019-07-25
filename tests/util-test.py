from heorot.utils import _test_match

_test_match("^user/{name}/{action}/?$","user/ben/update/")
_test_match("^.*/style.css","/next/style.css")
_test_match("^/?$","/")