import socket
import argparse
import sys
import json
import os
from datetime import datetime

HOST = "127.0.0.1"
PORT = 1060
MAX_BYTES = 65535

class Server:
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port


    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface, self.port))
        sock.listen(1)

        print(f"[SERVER] started and listens at {sock.getsockname()}")
        print()

        while True:
            try:
                sc, sockname = sock.accept()
                print("=" * 50)
                print(f"Accepted a connection from {sockname}")
                print(f"Socket name: {sc.getsockname()}")
                print(f"Socket peer: {sc.getpeername()}")
                print()

                todos = []

                data = sc.recv(MAX_BYTES).decode('ascii')

                if data == "start_list_session":
                    todo = sc.recv(MAX_BYTES).decode('ascii')
                    todos.append(todo)

                elif data == "end_list_session":
                    sc.close()
                    del todos
                    break

                elif data == "show_list":
                    dates = show_list(todos)
                    for date in dates:
                        print(date)

            except Exception as e:
                print("Error occurred!..")

            except OSError as e:
                print(f"Oops... {e.__class__} occurred. Failure in network transmission.")

            finally:
                sc.close()


    def show_list(self, todos):
        todos_ = []
        times = []

        for todo in todos:
            todo_ = todo.split('-')
            time = new_todo[0]
            times.append(time)

        times.sort(key=lambda date: datetime.strptime(date,'%H:%M'))
        return times

        
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        while True:
            data = input()
            sock.sendall(str.encode(data))
        
def main():
    choices = {'client':Client,'server':Server}
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=choices)
    parser.add_argument('host')
    parser.add_argument('-p', type=int, default=PORT)

    args=parser.parse_args()

    if args.role=='client':
        obj = Client(args.host, args.p)
        obj.start()
    if args.role=='server':
        obj = Server(args.host, args.p)
        obj.start()

if __name__=='__main__':
    main()