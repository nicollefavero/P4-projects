#!/bin/bash

python3 ./QUIC-flood/counter/run.py -s 2 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 ./QUIC-flood/counter/run.py -s 4 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 ./QUIC-flood/counter/run.py -s 8 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 ./QUIC-flood/counter/run.py -s 16 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 ./QUIC-flood/counter/run.py -s 32 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;

python3 /QUIC-flood/counter/run.py -s 2 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 4 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 8 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 16 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 32 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;

python3 /QUIC-flood/counter/run.py -s 2 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 4 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 8 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 16 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-flood/counter/run.py -s 32 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;

python3 /QUIC-Tr4ck/counter/run.py -s 2 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 4 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;

python3 /QUIC-Tr4ck/counter/run.py -s 2 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 4 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-flood/test_01;

python3 /QUIC-Tr4ck/counter/run.py -s 2 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 4 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 8 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 16 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 32 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;

python3 /QUIC-Tr4ck/counter/run.py -s 2 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 4 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 8 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 16 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 32 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;

python3 /QUIC-Tr4ck/counter/run.py -s 2 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 4 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 8 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 16 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 32 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;

python3 /QUIC-Tr4ck/counter/run.py -s 2 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 4 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;

python3 /QUIC-Tr4ck/counter/run.py -s 2 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
python3 /QUIC-Tr4ck/counter/run.py -s 4 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/server-logs/QUIC-Tr4ck/test_01;
