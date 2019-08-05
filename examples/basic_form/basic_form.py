from heorot.heorot2 import Hall, Response
from heorot.decorators import view, static
from heorot.utils import redirect, parse_query

# inmemory = {}

class BasicForm(Hall):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = [("^/?$", self.basehome),
                   (".*/?style.css", self.handle_static_css),
                   ("^show-all/?$", self.show_all),
                   ("^handle-form/?$", self.handle_form)]

        self.inmemory = {"names":[]}


    @view("header.html", "home-form.html")
    def basehome(self, request):
        return {"content":""}

    @static("text/css")
    def handle_static_css(self, request):
        return "style.css"

    @view("header.html", "show-all.html")
    def show_all(self, request):
        s = "<tr><td>{}</td><td>{}</td></tr>"
        rows = "\n".join([s.format(row[0], row[1]) for row in self.inmemory["names"]])
        return {"content": "test!", "rows":rows}

    @view(None, None)
    def handle_form(self, request):
        print(request.content)
        qd = parse_query(request.content)
        self.inmemory["names"].append((qd["firstname"], qd["lastname"]))
        print(self.inmemory)
        return {"content": self.handle(redirect(request, "/")).body}

if __name__ == '__main__':
    n = BasicForm()
    n.run()