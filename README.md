# UDPack

[![API-Docs-status](https://img.shields.io/github/actions/workflow/status/uncertainty-cc/UDP-Python/build-docs.yaml?branch=main&style=flat-square&label=Docs&logo=googledocs&logoColor=fff)](https://tk233.xyz/UDPack/udpack.html)

UDPack is a minimal Python wrapper around UDP sockets. It provides a single `UDP` class that acts as a full-duplex communication channel—bind an address to receive, specify a target to send, or do both.

Designed for lightweight robotics, networking utilities, and quick prototypes.

## Installation

```bash
pip install udpack
```

## Usage

```python
import numpy as np
from udpack import UDP

# Full duplex: listen on 8000, send to 8001
udp = UDP(recv_addr=("0.0.0.0", 8000), send_addr=("127.0.0.1", 8001))

# Raw bytes
udp.send(b"hello")
data = udp.recv()  # None on timeout

# Dict (JSON)
udp.send_dict({"x": 1.0, "y": 2.0})
obj = udp.recv_dict()

# NumPy arrays
udp.send_numpy(np.array([1, 2, 3], dtype=np.float32))
arr = udp.recv_numpy(dtype=np.float32)

udp.stop()
```

### Constructor

- **`recv_addr`** — `(host, port)` to bind and listen; `None` for transmit-only.
- **`send_addr`** — `(host, port)` of the remote peer; `None` for receive-only.

### Timeouts

Pass `timeout` to `recv`, `recv_dict`, or `recv_numpy`:

- `None` — blocking (wait forever)
- `0` — non-blocking (~0.1s poll)
- `> 0` — block for that many seconds

### API

| Method | Description |
|--------|-------------|
| `recv` / `send` | Raw bytes |
| `recv_dict` / `send_dict` | JSON-serialized dicts |
| `recv_numpy` / `send_numpy` | NumPy arrays (configurable `dtype`) |
| `stop` | Close the socket |
