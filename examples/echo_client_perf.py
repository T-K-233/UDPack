import time

from udpack import UDP


udp = UDP(recv_addr=("0.0.0.0", 8001), send_addr=("127.0.0.1", 8000))

counter = 0

udp.send("Hello, World: {counter}".encode())

while True:
    t = time.perf_counter()
    for i in range(1000):
        data = udp.recv()
        counter += 1
        udp.send(f"Hello, World: {counter}".encode())
    print(f"Round trip time: {time.perf_counter() - t:.4f} ms")

