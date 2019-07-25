import socket
import re
from .utils import parse_url

"""
A basic packet class for easy string sending.
"""
class Packet:
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


class Hall:
    def __init__(self, hostname='', port=8080, debug=False):
        self.port = port
        self.hostname = hostname
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # so you can reboot quicker
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.debug=debug

    def run(self):
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
                msg = msg[0].decode("utf-8").split(" ")[1][1:]

                path, query = parse_url(msg)

                response_body, status, headers = self.handle(path, query)
                print("receiving connection from {} : {}\t{}".format(addr[0], addr[1],path[:20]))

                packet = Packet(response_body=response_body)
                packet.response_headers.update(headers)
                packet.response_status = status

                c.sendall(packet.encode())
                c.close()
            except KeyboardInterrupt:
                break
        print("\nclosing connection on port {}".format(str(self.port)))

    def view(self, template, d):
        for key in d:
            template = template.replace("[[{}]]".format(key), d[key])
        return template

    def handle(self, path, query):
        response_body='<h1>I am not yet implemented</h1>'
        return response_body, '200', {}
