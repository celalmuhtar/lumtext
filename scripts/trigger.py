#!/usr/bin/env python3
import socket
import sys

try:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect("/tmp/lumtext.sock")
    s.sendall(b"trigger")
    s.close()
except Exception:
    sys.exit(1)
