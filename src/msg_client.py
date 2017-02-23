import argparse
import datetime
import random
import socket
import string
import time

BUFFER_SIZE = 2048
ENCODING = 'ascii'
MSG_SIZE = 1200

threads = {}
to_join = []

parser = argparse.ArgumentParser(description="Msg client")
parser.add_argument("-s", "--sleep", type=float, help="sleep time between two sendings", default=5.0)
parser.add_argument("-n", "--nb", type=int, help="number of requests done", default=5)
parser.add_argument("-B", "--bulk", type=bool, help="if set, don't wait for reply to send another packet", default=False)

args = parser.parse_args()


def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Handle reusing the same 5-tuple if the previous one is still in TIME_WAIT
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# Bind the socket to the port
server_address = ('10.1.0.1', 8000)
print("Try to connect to %s port %s" % server_address)
sock.connect(server_address)

delays = []

try:
    for i in range(args.nb):
        time.sleep(args.sleep)
        request = string_generator(size=MSG_SIZE, chars=string.digits)
        start_time = datetime.datetime.now()
        sock.sendall(request.encode(ENCODING))

        if args.bulk:
            continue

        buffer_data = ""
        while len(buffer_data) < MSG_SIZE:
            data = sock.recv(BUFFER_SIZE).decode(ENCODING)

            if len(data) == 0:
                # Connection closed at remote; close the connection
                break

            buffer_data += data

        if len(buffer_data) == MSG_SIZE:
            stop_time = datetime.datetime.now()
            delays.append(stop_time - start_time)
        else:
            print("An issue occured...")
            break
finally:
    # Clean up the connection
    print("Closing connection")
    sock.close()
    print(delays)
