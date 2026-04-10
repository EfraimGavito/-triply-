# client.py 
from socket32 import create_new_socket

HOST = '127.0.0.1'
PORT = 65431


def main():

    location = input('Where would you like to go? ')

    # Create socket to connect to the server

    with create_new_socket() as s:
        s.connect(HOST, PORT)

        s.sendall(location)

        while True:
            location = s.recv()
            print(location)
            break

if __name__ == '__main__':
    main()
