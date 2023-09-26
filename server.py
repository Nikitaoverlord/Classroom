import random
import socket
import _pickle as pickle
from _thread import *

HOST = None
PORT = None
#
###
# Creating SERVER
###
host_name = socket.gethostname()
HOST = socket.gethostbyname(host_name)

# Get an available port by opening a server with a port of 0 which will give it an available port (unless all are occupied),
# then get that port number and create the actual server
temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp_server.bind(('', 0))
PORT = temp_server.getsockname()[1]
temp_server.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((HOST, PORT))
    print(HOST, PORT)
except socket.error as problem:
    print(str(problem))
    quit()
###
###
###

###
### Begin Server-Client relationships
###
server.listen()

clients = {}  # {1:"127.0.0.1"} # id to ip
global_id = 1

while True:
    user_socket, address = server.accept()
    print(address[0] + " connected")

    clients[global_id] = address

    start_new_thread(client_thread, (user_socket, global_id))

    global_id += 1


def client_thread(user, user_id):
    while True:
        try:
            data = user.recv(2048 * 4)  # list of lists
            if not data:  # if no data is being recieved, user has disconnected from server
                break

            relay_data = pickle.dumps(())
            user.send(relay_data)

        except Exception as error:
            print("Error:", error)
            break

    del clients[user_id]
    user.close()
    print(f"USER CLOSED [id #{id}]")
###
###
###
