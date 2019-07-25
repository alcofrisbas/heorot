from heorot.heorot import Hall
from heorot.utils import match_path

# no additional paths: ^user/[^/]*/update/?$
TEMPLATE_DIR = "template/"
STATIC_DIR = "static/"

class Basic(Hall):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inmemory = {"names":[]}

    def retrieve(self,tname):
        with open(TEMPLATE_DIR+tname) as r:
            t = r.read()
        return t

    def static(self,tname):
        with open(STATIC_DIR+tname) as r:
            t = r.read()
        return t

    def homepage(self):
        s =  self.retrieve("home-form.html")
        d = {"content":s}
        template = self.retrieve("header.html")
        return self.view(template, d)


    def handle_home_form(self, qd):
        self.inmemory["names"].append((qd["firstname"], qd["lastname"]))
        #redirect to home
        s, _, __  =self.handle('', {})
        return s

    def nextpage(self):
        s =  """
        <h2>next</h2><table>{}</table>
        <a href="/">home</a>
        """.format("\n".join(["<tr><td>{}</td><td>{}</td></tr>".format(i[0], i[1]) for i in self.inmemory["names"]]))
        d = {"content":s}
        template = self.retrieve("header.html")
        return self.view(template, d)

    def handle(self, path, query):
        s = ""
        status = '200'
        headers = {}
        if match_path("^/?$", path):
            print("match home")
            s = self.homepage()
        elif match_path("next/?$", path):
            print("match next")
            s = self.nextpage()
        elif match_path("handle-home-form/?$",path):
            print("match form")
            s = self.handle_home_form(query)
        # match css
        elif match_path(".*.css", path):
            s = self.static(path.split("/")[-1])
            headers["Content-Type"] = "text/css"
        else:
            print("did not match {}".format(path))
            status = '404'
        return s, status, headers

if __name__ == '__main__':
    b = Basic()
    b.run()