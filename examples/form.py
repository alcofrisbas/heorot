from heorot.heorot import Hall

class Basic(Hall):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inmemory = {"names":[]}

    def homepage(self):
        return """
        <h1>home</h1>
        <form action="handle-home-form">
        First name:<br>
        <input type="text" name="firstname"><br>
        Last name:<br>
        <input type="text" name="lastname">
        <input type="submit" value="Submit">
        </form>
        """

    def handle_home_form(self, qd):
        print("HANDLE")
        self.inmemory["names"].append((qd["firstname"], qd["lastname"]))
        s, _, __  =self.handle('', {})
        ret = "".join(s)
        return ret

    def nextpage(self):
        s =  """
        <h2>next</h2>{}
        <a href="..">home</a>
        """.format("\n".join(["<p>{}   {}</p>".format(i[0], i[1]) for i in self.inmemory["names"]]))
        return s

    def handle(self, path, query):
        s = ""
        status = 200
        if path == "":
            print("handling home: {}".format(str(query)))
            s = self.homepage()
        elif path == "next":
            s = self.nextpage()
        elif path=="handle-home-form":
            s = self.handle_home_form(query)
        return [s], 200, {}

if __name__ == '__main__':
    b = Basic()
    b.run()