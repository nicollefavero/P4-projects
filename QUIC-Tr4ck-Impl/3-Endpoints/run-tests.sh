#!/bin/bash

FLOOD_SCRIPT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/3-Endpoints/QUIC-flood/run.py
TRACK_SCRIPT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/3-Endpoints/QUIC-Tr4ck/run.py

FLOOD_OUTPUT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/3-Endpoints/QUIC-flood
TRACK_OUTPUT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/3-Endpoints/QUIC-Tr4ck

BASELINE_OUTPUT_PATH=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/3-Endpoints/Baseline

CHARTS_SCRIPT=/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/Logs-Graphs/3-Endpoints

#python3 $TRACK_SCRIPT_PATH -d $BASELINE_OUTPUT_PATH -r 16 -i 1;
#python3 $TRACK_SCRIPT_PATH -d $BASELINE_OUTPUT_PATH -r 32 -i 1;

#python3 $TRACK_SCRIPT_PATH -s 2 -c 16 -t 1 -d $TRACK_OUTPUT_PATH -r 16 -i 1;
#python3 $TRACK_SCRIPT_PATH -s 4 -c 16 -t 1 -d $TRACK_OUTPUT_PATH -r 16 -i 1;
#python3 $TRACK_SCRIPT_PATH -s 8 -c 16 -t 1 -d $TRACK_OUTPUT_PATH -r 16 -i 1;

#python3 $TRACK_SCRIPT_PATH -s 2 -c 32 -t 1 -d $TRACK_OUTPUT_PATH -r 32 -i 1;
#python3 $TRACK_SCRIPT_PATH -s 4 -c 32 -t 1 -d $TRACK_OUTPUT_PATH -r 32 -i 1;

python3 $FLOOD_SCRIPT_PATH -s 2 -c 16 -t 1 -d $FLOOD_OUTPUT_PATH -r 16 -i 1;
python3 $FLOOD_SCRIPT_PATH -s 4 -c 16 -t 1 -d $FLOOD_OUTPUT_PATH -r 16 -i 1;
python3 $FLOOD_SCRIPT_PATH -s 8 -c 16 -t 1 -d $FLOOD_OUTPUT_PATH -r 16 -i 1;

#python3 $FLOOD_SCRIPT_PATH -s 2 -c 32 -t 1 -d $FLOOD_SCRIPT_PATH -r 32 -i 1;
#python3 $FLOOD_SCRIPT_PATH -s 4 -c 32 -t 1 -d $FLOOD_SCRIPT_PATH -r 32 -i 1;

cd CHARTS_SCRIPT;
python3 generate-charts.py -i Baseline/r16-i1 QUIC-flood/r16-i1 QUIC-Tr4ck/r16-i1 -l 2 4 8 -o 3tp-r16-i1-chart;
#python3 generate-charts.py -i Baseline/r32-i1 QUIC-flood/r32-i1 QUIC-Tr4ck/r32-i1 -l 4 8 -o 3tp-r32-i1-chart;
