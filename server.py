# server.py

import random
import client as clib
from socket32 import create_new_socket

HOST = '127.0.0.1'
PORT = 65431



def generate_flight_price():
    return

def generate_car_ride_price():
    return

def generate_food_delivery_price():
    return



def main():

# Create socket to connect the server to the client

    with create_new_socket() as s:

        s.bind(HOST, PORT)
        s.listen()
        print("Triply server started. Listening on", (HOST, PORT))

        conn2client, addr = s.accept()
        print('Connected by', addr)

        # Some testing stuff

        with conn2client:

            location = conn2client.recv()
            location = "Alrighty! " + location + " it is!"

            conn2client.sendall(location)

        


if __name__ == '__main__':
    main()
