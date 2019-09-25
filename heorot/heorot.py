import socket
import re
from .utils import parse_url
from .decorators import view

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
            'Content-Length': 0
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
        return s.encode(encoding)

class Request:
    def __init__(self, path, query, content, method, header):
        self.path = path
        self.query = query
        self.content = content
        self.method = method
        self.header = header
# TODO:  incorporate with Packet class
class Response:
    def __init__(self, response_body, status, headers):
        self.body = response_body
        self.status = status
        self.headers = headers


class Messenger:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class Hall:
    """
    Main framework class.
    """
    def __init__(self, hostname='', port=8080, debug=False):
        self.port = port
        self.hostname = hostname
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.debug=debug
        self.mapping = [("^/?$", self.base_home)]


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
                header = {}
                try:
                    for item in msg[0].decode("utf-8").strip().split("\r\n")[1:]:
                        # print(item)
                        head = [i.strip() for i in item.split(":")]
                        header[head[0]] = head[1]
                except:
                    pass
                # print(header)
                url = msg[0].decode("utf-8").split(" ")[1][1:]
                method = msg[0].decode("utf-8").split(" ")[0]
                try:
                    content = msg[0].decode("utf-8").split(" ")[-1].split("\n")[-1]
                except:
                    content = ""

                path, query = parse_url(url)

                request = Request(path, query, content,method, header)

                response = self.handle(request)
                print("receiving connection from {}{} : {}\t{}{}".format(green,addr[0], addr[1],path[:20], defcol))

                packet = Packet(response_body=response.body)
                packet.response_headers.update(response.headers)
                packet.response_status = response.status

                c.sendall(packet.encode())
                c.close()
            except KeyboardInterrupt:
                break
        print("\nclosing connection on port {}".format(str(self.port)))


    @view(None, None)
    def base_home(self, request):
        return {"content":"<h1>Hall not yet implemented</h1>"}



    def handle(self, request):
        """
        Main control method. Implemented by user
        :param: path str
        :param: query dict
        :param content str
        """

        response_body = ""
        header = {}
        for m in self.mapping:
            if re.match(m[0], request.path):
                response_body, header = m[1](request)
        return Response(response_body, '200', header)

