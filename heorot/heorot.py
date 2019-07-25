import socket
import re
from .utils import parse_url

# pretty colors
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
defcol = "\033[0m"


class Packet:
    """
    A basic packet class for easy string sending.
    """
    def __init__(self, response_body=""):
        # set up headers
        self.response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': 0,
        }
        self.response_body = response_body
        self.response_proto = 'HTTP/1.1'
        self.response_status = '200'
        self.response_status_text = 'OK'

    # encode for sending and concat all data
    def encode(self,encoding="utf-8"):
        self.response_headers['Content-Length'] = len(self.response_body)
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                               self.response_headers.items())
        proto = self.response_proto + " " + self.response_status + ' ' + self.response_status_text + "\n"

        s = proto + response_headers_raw + "\n" + self.response_body
        # print(s)
        return s.encode(encoding)

# not used yet.
class Request:
    def __init__(self, path, query, content, method):
        self.path = path
        self.query = query
        self.content = content
        self.method = method


class Hall:
    #comment inline
    """
    Main framework class.
    """
    def __init__(self, hostname='', port=8080, debug=False):
        self.port = port
        self.hostname = hostname
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # so you can reboot quicker
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.debug=debug
        self.TEMPLATE_DIR = "template/"
        self.STATIC_DIR = "static/"


    def run(self):
        """
        Runs the server mainloop. Calls handle() on every connection.
        """
        self.s.bind((self.hostname, self.port))
        self.s.listen(5)
        print("listening on '{}', {}".format(self.hostname, self.port))

        while True:
            try:
                c, addr = self.s.accept()
                msg = c.recvmsg(4096)
                # for debug...
                if self.debug:
                    print(msg)
                url = msg[0].decode("utf-8").split(" ")[1][1:]
                method = msg[0].decode("utf-8").split(" ")[0]
                try:
                    content = msg[0].decode("utf-8").split(" ")[-1].split("\n")[-1]
                except:
                    content = ""

                path, query = parse_url(url)

                request = Request(path, query, content,method)

                response_body, status, headers = self.handle(request)
                print("receiving connection from {}{} : {}\t{}{}".format(green,addr[0], addr[1],path[:20], defcol))

                packet = Packet(response_body=response_body)
                packet.response_headers.update(headers)
                packet.response_status = status

                c.sendall(packet.encode())
                c.close()
            except KeyboardInterrupt:
                break
        print("\nclosing connection on port {}".format(str(self.port)))

    def view(self, template, d):
        """
        Fills a template with a dictionary
        :param: template str
        :param: d dict
        """
        for key in d:
            template = template.replace("[[{}]]".format(key), d[key])
        return template

    def handle(self, request):
        """
        Main control method. Implemented by user
        :param: path str
        :param: query dict
        :param content str
        """
        response_body='<h1>I am not yet implemented</h1>'
        return response_body, '200', {}

    def retrieve(self,tname):
        """
        Retrieves a template from TEMPLATE_DIR
        :param: tname str
        """
        with open(self.TEMPLATE_DIR+tname) as r:
            t = r.read()
        return t

    def static(self,tname):
        """
        Retrieves a static file from STATIC_DIR
        :param: tname str
        """
        with open(self.STATIC_DIR+tname) as r:
            t = r.read()
        return t
