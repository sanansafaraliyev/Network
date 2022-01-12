import socket
import argparse
import json

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

        print("Listening at", sock.getsockname())
        sc, address = sock.accept()

        items = []

        while True:
            try:
                data = sc.recv(MAX_BYTES).decode('ascii')

                if data == "start":
                    print("Process starts..")
                elif data == "show_items":
                    result = self.unique(self.sorted_items(items))
                    result_dumped = json.dumps(result)
                    sc.send(result_dumped.encode('ascii')) 
                elif data == "end":
                    sc.close()
                    break
                else:
                    items.append(data)
            except ValueError:
                continue

    def sorted_items(self, items):
        copy_items = items
        items_sorted = []

        item_count = 0

        for item in copy_items:
            item_count = copy_items.count(item)
            items_sorted.append(tuple((item, item_count)))
        
        return items_sorted

    def unique(self, any_list):
        unique_sorted = []

        for i in any_list:
            if i not in unique_sorted:
                unique_sorted.append(i)

        return unique_sorted


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        print("Client has been assigned hostname", sock.getsockname())

        while True:
            data = input()
            sock.sendall(data.encode('ascii'))
            if data == "show_items":     
                data_received = sock.recv(MAX_BYTES).decode('ascii')
                data_to_show = json.loads(data_received)
                #print(data_to_show)
                for i in data_to_show:
                    print(i)
            elif data == "end":
                sock.close()
                break


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
    