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

def sanitize(html):
    # remove tags
    html = re.sub("</?(.*?)>", "", html)
    # remove comment open
    html = re.sub("</?", "", html)
    return html


def parse_query(query):
    queryList = query.split("&")
    queryDict = parse_qs(query)
    for q in queryDict:
        queryDict[q] = sanitize(queryDict[q][0])
    return queryDict

def parse_url(url):
    o = urlparse(url)
    queryDict = parse_query(o.query)
    return  o.path, queryDict

def _test_match(template, actual):
    p = match_path(template,actual)
    if p:
        print(p)
    else:
        print("not a match")

def redirect(request, path):
    request.path = path
    return request

def retrieve(fname):
    with open(fname) as r:
        t = r.read()
    return t