from udpack import UDP


udp = UDP(recv_addr=("0.0.0.0", 8000), send_addr=("127.0.0.1", 8001))

while True:
    data = udp.recv()
    print(f"Received: {data}")
    udp.send(data)

