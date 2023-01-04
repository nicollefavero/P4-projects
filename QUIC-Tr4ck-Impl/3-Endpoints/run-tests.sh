#!/bin/bash

FLOOD_SCRIPT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/3-Endpoints/QUIC-flood/run.py
TRACK_SCRIPT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/3-Endpoints/QUIC-Tr4ck/run.py

FLOOD_OUTPUT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/3-Endpoints/QUIC-flood
TRACK_OUTPUT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/3-Endpoints/QUIC-Tr4ck



python3 $TRACK_SCRIPT_PATH -s 2 -c 2 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 4 -c 2 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 8 -c 2 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 16 -c 2 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 32 -c 2 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;

python3 $TRACK_SCRIPT_PATH -s 2 -c 4 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 4 -c 4 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 8 -c 4 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 16 -c 4 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 32 -c 4 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;

python3 $TRACK_SCRIPT_PATH -s 2 -c 8 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 4 -c 8 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 8 -c 8 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 16 -c 8 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;

python3 $TRACK_SCRIPT_PATH -s 2 -c 16 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 4 -c 16 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;

python3 $TRACK_SCRIPT_PATH -s 2 -c 32 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
python3 $TRACK_SCRIPT_PATH -s 4 -c 32 -t 1 -d $TRACK_OUTPUT_PATH -r 2 -i 1;
