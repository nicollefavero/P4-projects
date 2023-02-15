#!/bin/bash

for i in 1
do
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 2 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 4 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 8 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 16 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 32 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 2 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 4 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 8 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 16 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 32 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 2 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 4 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 8 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 16 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;


  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 2 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 4 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 2 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/run.py -s 4 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-flood/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 2 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 4 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 8 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 16 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 32 -c 2 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 2 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 4 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 8 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 16 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 32 -c 4 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 2 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 4 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 8 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 16 -c 8 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 2 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 4 -c 16 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;

  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 2 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
  python3 /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/run.py -s 4 -c 32 -t 1 -o /home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/QUIC-Tr4ck/test_0$i;
done
