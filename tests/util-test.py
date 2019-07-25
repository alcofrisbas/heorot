from heorot.utils import _test_match, sanitize

_test_match("^user/{name}/{action}/?$","user/ben/update/")
_test_match("^.*/style.css","/next/style.css")
_test_match("^/?$","/")

print(sanitize('<script>function f(){alert("xss");}window.onload=f;</script>'))
print(sanitize('<<script>function f(){alert("xss");}window.onload=f;<</script>'))
print(sanitize('<b>INJECT</b>'))
print(sanitize('<!--'))