import re
from urllib.parse import urlparse, parse_qs

# sees if template matches
def match_path(template, actual):
    match_template = "{(.*?)}"
    match_actual = re.sub("{(.*?)}", "[^/]*", template)
    # print(match_actual)
    matches = re.findall(match_actual, actual)
    if matches:
        return True
    return False


# assuming we get a path that is solely paths, no query!
# match keys in template to actual
def match_path_keys(template, actual):
    if not match_path(template, actual):
        return False
    template_list = template.strip("/?$").split("/")
    actual_list = actual.strip("/").split("/")
    d = {}
    for i, j in zip(template_list, actual_list):
        if not re.match("{(.*?)}",i):
            if i != j:
                return False
        else:
            d[i[1:-1]] = j
    return d

def parse_url(url):
    o = urlparse(url)
    queryList = o.query.split("&")
    queryDict = parse_qs(o.query)
    for q in queryDict:
        queryDict[q] = queryDict[q][0]
    return  o.path, queryDict

def _test_match(template, actual):
    p = match_path(template,actual)
    if p:
        print(p)
    else:
        print("not a match")

if __name__ == '__main__':
    # print (match_path_old("user/{name}/{action}/?$","user/ben/update/"))
    _test_match("^user/{name}/{action}/?$","user/ben/update/")
    _test_match("^.*/style.css","/next/style.css")
    _test_match("^/?$","/")
