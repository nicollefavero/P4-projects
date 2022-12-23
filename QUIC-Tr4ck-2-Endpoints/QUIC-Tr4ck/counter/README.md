# Implementing Basic Forwarding With in a HTTP/3 (QUIC) Client-Server

## Introduction

The objective of this program is to forward packets from a HTTP/3 client to a
HTTP/3 server using QUIC. The code for both client and server, as well as the
necessary python code for this to work was taken from aioquic repository. Despite
small changes in the network topology, the code for the switch and for the mininet topology was taken from p4-tutorial repository.


>The P4 program will be written for the V1Model architecture implemented
on P4.org's bmv2 software switch. The architecture file for the V1Model
can be found at: /usr/local/share/p4c/p4include/v1model.p4. This file
desribes the interfaces of the P4 programmable elements in the architecture,
the supported externs, as well as the architecture's standard metadata
fields. We encourage you to take a look at it.

# Environment
It is necessary to install the following python libraries:
- wsproto
- aioquic
- httpbin
- werkzeug==2.0.3
- flask
- asgiref
- starlette

To install from the `requirements.txt` run:
"""
pip install -r requirements.txt
"""

## Run the P4 program and start the Mininet
To run the program:
"""
make run
"""

To stop the Mininet instance in background:
"""
make stop
"""

After use, to clean the environment:
"""
make clean
"""

## Inside Mininet
"""
xterm h1 h2
"""

In `h2` run to following command to use it as a server:
"""
./receive.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem
"""

In `h1` run to following command to use it as a client:
"""
./send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/
"""

## Relevant Documentation

The documentation for P4_16 and P4Runtime is available [here](https://p4.org/specs/)

All excercises in this repository use the v1model architecture, the documentation for which is available at:
1. The BMv2 Simple Switch target document accessible [here](https://github.com/p4lang/behavioral-model/blob/master/docs/simple_switch.md) talks mainly about the v1model architecture.
2. The include file `v1model.p4` has extensive comments and can be accessed [here](https://github.com/p4lang/p4c/blob/master/p4include/v1model.p4).
