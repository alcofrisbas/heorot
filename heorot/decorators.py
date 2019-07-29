# TODO: non-hard coded template and static dirs
from .utils import retrieve as _retrieve

class view:
    def __init__(self, template, doc):
        """
        template: the main template eg menus
        doc: the html page in which dynamic content
        is inserted.
        """
        self.template = template
        self.doc = doc
        self.template_dir = "template/"

    def __call__(self, control):
        def fw(*args):
            d = control(*args)
            if not self.template or not self.doc:
                return d["content"], {"Content-Type": "text/html"}
            template = _retrieve(self.template_dir + self.template)
            doc_content = _retrieve(self.template_dir + self.doc)
            for key in d:
                doc_content = doc_content.replace("[[{}]]".format(key), d[key])
            template = template.replace("[[doc_content]]", doc_content)
            return template, {"Content-Type": "text/html"}
        return fw

class static:
    def __init__(self, content_type):
        self.static_dir = "static/"
        self.content_type = content_type

    def __call__(self, control):
        def fw(*args):
            s = control(*args)
            ret = _retrieve(self.static_dir+s)
            return ret, {"Content-Type": self.content_type}
        return fw