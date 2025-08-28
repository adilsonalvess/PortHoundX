import pytest
import socket
import subprocess
import sys
import os

# Import the main script (assuming it's named porthoundx.py)
import src.porthoundx as porthoundx

# -------------------------------
# Helpers
# -------------------------------
def is_port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except Exception:
        return False

# -------------------------------
# Tests
# -------------------------------

def test_public_ip_ping():
    """Google DNS should respond to ping."""
    result = porthoundx.ping_host("8.8.8.8")
    assert result is True

def test_dns_resolution():
    """Domain name should resolve to IP."""
    ip = porthoundx.resolve_dns("example.com")
    assert ip is not None
    assert isinstance(ip, str)

def test_port_80_open():
    """example.com should have port 80 open."""
    result = is_port_open("example.com", 80)
    assert result is True

def test_private_ip_detection():
    """Private IP should be flagged as private."""
    assert porthoundx.is_private_ip("192.168.1.1") is True

def test_public_ip_detection():
    """Public IP should be flagged as public."""
    assert porthoundx.is_private_ip("8.8.8.8") is False

def test_cli_execution():
    """Check CLI runs without crash."""
    result = subprocess.run(
        [sys.executable, "porthoundx.py", "--host", "8.8.8.8", "--ports", "22,80"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Host:" in result.stdout
