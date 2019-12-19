import pickle
import struct
import sys
import numpy as np
from socket import *

def send_from(arr, dest):
    view = memoryview(arr).cast('B')
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]

def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]

s = socket(AF_INET, SOCK_STREAM)
s.bind(('10.0.11.46', 25000))
print('Listening to the port 25000')
s.listen()
c, a = s.accept()

while True:  
    #server memory is a pre-assigned memory area, we only change the contains in it
    server_memory = np.zeros(shape = (300, 300, 3), dtype = float)
    recv_into(server_memory, c)
    print(server_memory)
    server_memory = 1-server_memory
    send_from(server_memory, c)
    # we must firstly define the scale of the array, and put the received item
    # into the prelocated memory.
    
    instruction = c.recv(1024).decode()
    if instruction == 'y':
        print("Client shutdown the connection, listening to the port...")
        s.listen()
        c, a = s.accept()
    
    else:
        print("Connection continue")
    
