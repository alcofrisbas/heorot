from heorot.heorot import Hall

class Basic(Hall):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def homepage(self):
        return """
        <h1>home</h1>
        <a href="next/">next</a>
        """

    def nextpage(self):
        return """
        <h2>next</h2>
        <a href="..">home</a>
        """

    def handle(self, path, query):
        s = ""
        if path == "":
            s = self.homepage()
        elif path == "next/":
            s = self.nextpage()
        return [s]

if __name__ == '__main__':
    b = Basic()
    b.run()