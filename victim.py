from libs.shell import shell

ip = "127.0.0.1"
port = 1234

sh = shell(ip, port)
sh.connect()