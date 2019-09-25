from heorot.heorot import Hall
from heorot.decorators import view
from heorot.utils import redirect, parse_query
import hashlib
import random
def create_sessionid(l=10):
    r = ""
    chars=list("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM")
    for i in range(l):
        r += random.choice(chars)
    return r
# hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()

fake_db = {"users":[["ben", "password", None]]}

class Cookie(Hall):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = [("^/?$", self.home),
                        ("^login/?$", self.handle_login)]

    @view("header.html", "home-form.html")
    def home(self, request):
        cookie = request.header["Cookie"].split(";")
        c_dict = {}
        for i in cookie:
            if "=" in i:
                j = i.split("=")
                c_dict[j[0].strip()] = j[1].strip()
            else:
                c_dict[i.strip()] = True
        print("DICT",c_dict)
        s = "Guest"
        # print(c_dict["sessionid"])
        if c_dict.get("sessionid"):
            print("FOUND SESSIONID")
            for user in fake_db["users"]:
                print(c_dict["sessionid"], user[2])
                if c_dict["sessionid"] == user[2]:
                    s = user[0]
                    break

        return {"content":s, "header":{}}

    @view(None, None)
    def handle_login(self, request):
        qd = parse_query(request.content)
        print(qd)
        ret = {"content": self.handle(redirect(request, "/")).body}
        for user in fake_db["users"]:
            print(user)
            if qd["username"] == user[0] and qd["password"] == user[1]:
                user[2] = create_sessionid(32)
                d = {"header":{"Set-Cookie":"sessionid={}".format(user[2])}}
                ret.update(d)
                print(ret)
                break
        return ret


if __name__ == '__main__':
    n = Cookie()
    n.run()