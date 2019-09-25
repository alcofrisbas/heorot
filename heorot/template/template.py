"""
ideas:

denoting insert point:
variables: @var ?

commands: ::<command>:: ?
"""

class Name:
    def __init__(self, first, last):
        self.first = first
        self.last = last

s1 = "<p>Welcome, @name.first </p>"

s2="""<table>
<tbody>
:: @name in @names <tr><td> @name.first </td><td> @name.last </td></tr>::
</tbody>
<table>
"""
import re
def read(template, insert):
    print(re.findall(r"@\S+", template))


if __name__ == '__main__':
    name = Name("ben", "greene")
    read(s1, {"name": name})
    # read(s2, "adf")