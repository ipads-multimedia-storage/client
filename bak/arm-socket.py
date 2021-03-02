import socket
import json


def receive_message():
    address = ('0.0.0.0', 8003)
    # socket.SOCK_STREAM：for TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    # param: max connection number
    s.listen(1)

    def recvall(sock, count):
        buf = b''  # buf type: byte
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    conn, addr = s.accept()
    print('receiving side: accepted connection from '+str(addr))
    while 1:
        length = int(recvall(conn, 16).rstrip())
        response = json.loads(recvall(conn, length))
        average_bandwidth = response["avg"]
        print(average_bandwidth)


if __name__ == '__main__':
    receive_message()
