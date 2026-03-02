from udpack import UDP


udp = UDP(recv_addr=("0.0.0.0", 8001), send_addr=("127.0.0.1", 8000))

counter = 0

udp.send("Hello, World: {counter}".encode())

while True:
    data = udp.recv()
    print(f"Received: {data}")
    counter += 1
    udp.send(f"Hello, World: {counter}".encode())

