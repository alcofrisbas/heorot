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

    def style(self,tname):
        with open(STATIC_DIR+tname) as r:
            t = r.read()
        return t

    def homepage(self):
        css = self.style("style.css")
        s =  """
        <h1>home</h1>
        <form action="handle-home-form">
        First name:<br>
        <input type="text" name="firstname" required><br>
        Last name:<br>
        <input type="text" name="lastname" required>
        <input type="submit" value="Submit">
        </form>
        <a href="next/">view all</a>
        """
        d = {"style": css, "content":s}
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
        css = self.style("style.css")
        d = {"style": css, "content":s}
        template = self.retrieve("header.html")
        return self.view(template, d)

    def handle(self, path, query):
        s = ""
        status = 200
        if match_path(path, "$"):
            s = self.homepage()
        elif match_path(path, "next/?$"):
            s = self.nextpage()
        elif match_path(path,"handle-home-form/?$"):
            s = self.handle_home_form(query)
        return s, 200, {}

if __name__ == '__main__':
    b = Basic()
    b.run()