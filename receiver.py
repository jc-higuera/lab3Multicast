#!/usr/bin/env python

from __future__ import division
import cv2
import numpy as np
import socket
import struct

MAX_DGRAM = 2 ** 16


def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        #print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            #print("finish emptying buffer")
            break


def set_ip():
    """ Getting image udp frame &
        concate before decode and output image """

    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    multicast_group = input("Ingrese la dirección de multicast: ")
    port = int(input("Ingrese el puerto del servidor multicast: "))
    print("")
    s.bind(('0.0.0.0', port))

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    dat = b''
    dump_buffer(s)
    get_video(s, dat)


def get_video(s, dat):
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                s.close()
                set_ip()
                break
            dat = b''

    # cap.release()
    cv2.destroyAllWindows()
    s.close()


def main():
    set_ip()


if __name__ == "__main__":
    main()
