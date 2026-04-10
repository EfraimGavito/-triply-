# client.py 
from socket32 import create_new_socket

HOST = '127.0.0.1'
PORT = 65431


def main():

    print('Hello world')

    # Create socket to connect to the server

    with create_new_socket() as s:
        s.connect(HOST, PORT)

        s.sendall('richmond grim reaper')

        while True:
            nettspend = s.recv()
            print(nettspend)
            break

if __name__ == '__main__':
    main()# client.py

