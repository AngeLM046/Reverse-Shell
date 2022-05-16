from libs.lee32 import encrypt, decrypt
from libs.shell import shell

ip = "127.0.0.1"
port = 1234

print(f"Listening on port {[port]}..")
sh = shell(ip, port)
sh.listen()

sh.accept()
