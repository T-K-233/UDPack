"""Tests for udpack.UDP class using loopback communication."""

import socket

import numpy as np
import pytest

from udpack import UDP


def _free_port():
    """Return an available port on 127.0.0.1."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def port_pair():
    """Two adjacent free ports for bidirectional UDP tests."""
    base = _free_port()
    return (base, base + 1)


@pytest.fixture
def udp_pair(port_pair):
    """Create two UDP instances that can communicate over loopback."""
    port_a, port_b = port_pair
    udp_a = UDP(
        recv_addr=("127.0.0.1", port_a),
        send_addr=("127.0.0.1", port_b),
    )
    udp_b = UDP(
        recv_addr=("127.0.0.1", port_b),
        send_addr=("127.0.0.1", port_a),
    )
    yield udp_a, udp_b
    try:
        udp_a.stop()
    except OSError:
        pass
    try:
        udp_b.stop()
    except OSError:
        pass


class TestSendRecv:
    """Test send/recv byte, dict, and numpy methods."""

    def test_send_recv_bytes(self, udp_pair):
        udp_a, udp_b = udp_pair
        udp_a.send(b"hello")
        assert udp_b.recv() == b"hello"
        udp_b.send(b"world")
        assert udp_a.recv() == b"world"

    def test_send_recv_dict(self, udp_pair):
        udp_a, udp_b = udp_pair
        data = {"x": 1.0, "y": 2.0, "nested": {"a": 1}}
        udp_a.send_dict(data)
        assert udp_b.recv_dict() == data

    def test_send_recv_numpy(self, udp_pair):
        udp_a, udp_b = udp_pair
        arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        udp_a.send_numpy(arr)
        recv = udp_b.recv_numpy(dtype=np.float32)
        assert recv is not None
        np.testing.assert_array_equal(recv, arr)

    def test_send_recv_numpy_int32(self, udp_pair):
        udp_a, udp_b = udp_pair
        arr = np.array([1, 2, 3], dtype=np.int32)
        udp_a.send_numpy(arr)
        recv = udp_b.recv_numpy(dtype=np.int32)
        assert recv is not None
        np.testing.assert_array_equal(recv, arr)


class TestTimeout:
    """Test recv timeout behavior."""

    def test_recv_timeout_returns_none(self, udp_pair):
        udp_a, udp_b = udp_pair
        result = udp_b.recv(timeout=0.1)
        assert result is None

    def test_recv_dict_timeout_returns_none(self, udp_pair):
        udp_a, udp_b = udp_pair
        assert udp_b.recv_dict(timeout=0.1) is None

    def test_recv_numpy_timeout_returns_none(self, udp_pair):
        udp_a, udp_b = udp_pair
        assert udp_b.recv_numpy(timeout=0.1) is None


class TestConstructor:
    """Test rx-only and tx-only modes and validation."""

    def test_recv_without_recv_addr_raises(self):
        udp = UDP(recv_addr=None, send_addr=("127.0.0.1", 51999))
        with pytest.raises(ValueError, match="receive address"):
            udp.recv()
        udp.stop()

    def test_send_without_send_addr_raises(self):
        port = _free_port()
        udp = UDP(recv_addr=("127.0.0.1", port), send_addr=None)
        with pytest.raises(ValueError, match="send address"):
            udp.send(b"data")
        udp.stop()


class TestStop:
    """Test socket cleanup."""

    def test_stop_closes_socket(self, udp_pair):
        udp_a, udp_b = udp_pair
        udp_a.stop()
        udp_b.stop()
        with pytest.raises(OSError):
            udp_a.send(b"x")
        with pytest.raises(OSError):
            udp_b.recv()
