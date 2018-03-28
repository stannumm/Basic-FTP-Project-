
#server scripti
# alýndýðý site : https://pypi.python.org/pypi/pyftpdlib/

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", "C:/Users/ahmet/Desktop/FTP", perm="elradfmwMT")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 21), handler)
server.serve_forever()