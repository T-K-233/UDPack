import socket
import json

import numpy as np


class UDP:
    """
    UDP class for sending and receiving data from a UDP socket as a full duplex communcation channel.
    """
    def __init__(self, recv_addr=("127.0.0.1", 8000), send_addr=("127.0.0.1", 8001)):
        """
        Initialize UDP Tx and Rx
        
        Args:
            recv_addr: address to listen on, None if not receiving (tx only)
            send_addr: address of target host, None if not sending (rx only)
        """
        self.recv_addr = recv_addr
        self.send_addr = send_addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        if self.recv_addr:
            self._sock.bind(self.recv_addr)
            print("UDP Rx is initialized:", self.recv_addr)
        
        if self.send_addr:
            print("UDP Tx is initialized:", self.send_addr)

    def stop(self) -> None:
        """
        Close the socket.
        """
        self._sock.close()

    def recv(self, bufsize=1024, timeout=None) -> bytes:
        """
        Receive data

        timeout == None: blocking forever
        timeout == 0: non-blocking (the actual delay is around 0.1s)
        timeout > 0: blocking for timeout seconds

        Args:
            bufsize: size of data buffer to receive
            timeout: timeout in seconds
        """
        if not self.recv_addr:
            raise ValueError("Cannot receive data without a receive address")
        self._sock.settimeout(timeout)
        try:
            buffer, addr = self._sock.recvfrom(bufsize)
        except (socket.timeout, BlockingIOError):
            return None
        return buffer

    def send(self, buffer: bytes) -> None:
        """
        Send a byte buffer to the target device.
        
        Args:
            buffer: data to send
        """
        if not self.send_addr:
            raise ValueError("Cannot send data without a send address")
        self._sock.sendto(buffer, self.send_addr)

    def recv_dict(self, bufsize=1024, timeout=None) -> dict:
        """
        Receive data and deserialize it into a python dictionary.

        See `recv()` for more information on timeout.

        Args:
            bufsize: size of data buffer to receive
            timeout: timeout in seconds
        """
        buffer = self.recv(bufsize=bufsize, timeout=timeout)
        if not buffer:
            return None
        serialized_data = buffer.decode("utf-8")
        data = json.loads(serialized_data)
        return data
    
    def send_dict(self, data: dict) -> None:
        """
        Serialize a python dictionary and send it.
        
        Args:
            data: data to send
        """
        buffer = json.dumps(data)
        buffer = buffer.encode()
        self.send(buffer)

    def recv_numpy(self, bufsize=1024, dtype=np.float32, timeout=None) -> np.ndarray:
        """
        Receive data and deserialize it into a numpy array.
        
        See `recv()` for more information on timeout.
        
        Args:
            bufsize: size of data buffer to receive
            dtype: numpy data type
            timeout: timeout in seconds
        """
        buffer = self.recv(bufsize=bufsize, timeout=timeout)
        if not buffer:
            return None
        data = np.frombuffer(buffer, dtype=dtype)
        return data

    def send_numpy(self, data: np.ndarray) -> None:
        """
        Serialize a numpy array and send it.
        
        Args:
            data: data to send
        """
        buffer = data.tobytes()
        self.send(buffer)
