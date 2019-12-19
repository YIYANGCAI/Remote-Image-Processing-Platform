# client.py
import numpy as np
import sys
import pickle, struct
from socket import *
import cv2

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

c = socket(AF_INET, SOCK_STREAM)
c.connect(('10.0.11.46', 25000))
flag = True

frame = cv2.imread("0.jpg")
frame = cv2.resize(frame, (300, 300))
frame = frame/255.0

#cv2.imshow("before", client_memory)
#cv2.waitKey(0)

while flag:
    print("--------------------------------------------------")
    # client_memory = frame
    # allocate an area
    # each epoch the area must be re-allocated, or the 
    client_memory = np.zeros(shape = (300, 300, 3), dtype = float)
    cv2.imshow("before", frame)
    #cv2.waitKey(0)

    send_from(frame, c)
    recv_into(client_memory, c)

    cv2.imshow("after", client_memory)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #print(client_memory)

    
    msg = input("Would you like to shutdown the connection?[y/n]").strip()
    if msg == 'y':
        print("Connection closed")
        c.send(msg.encode())
        flag = False
    else:
        c.send(msg.encode())
    

c.close()

