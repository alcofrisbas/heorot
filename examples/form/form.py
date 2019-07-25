from heorot.heorot import Hall
from heorot.utils import match_path, parse_query, sanitize

# no additional paths: ^user/[^/]*/update/?$
# TEMPLATE_DIR = "template/"
# STATIC_DIR = "static/"

class Basic(Hall):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inmemory = {"names":[]}

    def homepage(self):
        s =  self.retrieve("home-form.html")
        d = {"content":s}
        template = self.retrieve("header.html")
        return self.view(template, d)


    def handle_home_form(self, qd):
        self.inmemory["names"].append((qd["firstname"], qd["lastname"]))
        #redirect to home
        s, _, __  =self.handle('', {},"")
        return s

    def nextpage(self):
        rows = "\n".join(["<tr><td>{}</td><td>{}</td></tr>".format(sanitize(i[0]),
                                                                   sanitize(i[1])) for i in self.inmemory["names"]])
        s = self.view(self.retrieve("show-all.html"), {"rows": rows})
        d = {"content":s}
        template = self.retrieve("header.html")
        return self.view(template, d)

    def handle(self, request):
        s = ""
        status = '200'
        headers = {}
        if match_path("^/?$", request.path):
            s = self.homepage()
        elif match_path("next/?$", request.path):
            s = self.nextpage()
        elif match_path("handle-home-form/?$",request.path):
            s = self.handle_home_form(parse_query(request.content))
        # match css
        elif match_path(".*.css", request.path):
            s = self.static(request.path.split("/")[-1])
            headers["Content-Type"] = "text/css"
        else:
            status = '404'
        return s, status, headers

if __name__ == '__main__':
    b = Basic()
    b.run()