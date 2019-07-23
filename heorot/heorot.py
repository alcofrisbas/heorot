import socket
from urllib.parse import urlparse

"""
A basic packet class for easy string sending.
"""
class Packet:
    def __init__(self, response_body=[]):
        # set up headers
        self.response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': 0,
            'Connection': 'close',
        }
        self.response_body = response_body
        self.response_proto = 'HTTP/1.1'
        self.response_status = '200'
        self.response_status_text = 'OK'

    # encode for sending and concat all data
    def encode(self,encoding="utf-8"):
        response_body_raw = ''.join(self.response_body)
        self.response_headers['Content-Length'] = len(response_body_raw)
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                               self.response_headers.items())
        proto = self.response_proto + " " + self.response_status + ' ' + self.response_status_text + "\n"

        s = proto + response_headers_raw + "\n" + response_body_raw
        return s.encode(encoding)



class Frame:
    def __init__(self, hostname='', port=8080):
        self.port = port
        self.hostname = hostname
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # so you can reboot quicker
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def parseUrl(self, url):
        o = urlparse(url)
        return  o.path, o.query.split("&")


    def run(self):
        self.s.bind((self.hostname, self.port))
        self.s.listen(5)
        print("listening on '{}', {}".format(self.hostname, self.port))

        while True:
            try:
                c, addr = self.s.accept()

                msg = c.recvmsg(4096)
                msg = msg[0].decode("utf-8").split(" ")[1][1:]


                path, query = self.parseUrl(msg)

                packet = Packet(response_body=self.handle(path, query))
                c.sendall(packet.encode())
                c.close()
            except KeyboardInterrupt:
                break
        print("\nclosing connection on port {}".format(str(self.port)))


    def handle(self, path, query):
        response_body=['<h1>I am not yet implemented</h1>']
        return response_body

if __name__ == '__main__':
    frame = Frame()
    frame.run()