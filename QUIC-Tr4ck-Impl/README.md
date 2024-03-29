# QUIC-Tr4ck Howto

## How the Experiments Are Organized
There are two scenarios for the experiments: one with a topology of 2 end systems, and another with 3 end systems. In both experiments there are only one switch which all end systems are connected to. Each of these scenarios has two experiments: one without mitigation, just the QUIC flood attack, and another with the mitigation technique, the QUIC-Tr4ck.    

All four experiments have the same directory structure:   

* `p4-src`: where all `P4`-related files are.   
* `quic-src`: where all `aioquic`-related files are, such as the scripts that run the QUIC client and the QUIC server as well as its dependencies (cloned from `aioquic` repository).   
* `utils`: here are all sort of scripts necessary to create and run the environment that emulates the programmable switch (cloned from `p4-tutorial` repository).   
* There are also two `python` scripts in the same directory level as stuff listed above: `run.py` and `generate-server-logs.py`. These scripts' goal is to automate everything, from `mininet` instantiation to experiments running and environment cleaning, and also logging.    

## Running a Test Case Manually

For the tutorial, I will be using `QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/` directory's content, but every step is reproducible within the other three experiments.   

Inside the folder `QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/p4-src`, there is a Makefile file that sets some variables and calls another Makefile in `QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/utils`. These Makefiles compile the P4 program `main.p4` and start the Mininet environment using all the configuration files from `p4-src/topology` and `utils`. But the commands are very simple:   

To enter the right directory:
```
cd QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/p4-src
```

To compile the P4 program and start the Mininet:
```
make run
```

After a lot of output in the terminal, you shall see the following line that expects you to enter commands in the Mininet environment:
```
mininet>
```

To actually run the experiment, we must run the server in a non-blocking way inside the Mininet. We will run the server on host `h2`:
```
h2 python3 ../quic-src/receive.py --certificate ../quic-src/tests/ssl_cert.pem --private-key ../quic-src/tests/ssl_key.pem &
```

Right after running the server, we are interested in seeing some metrics and logs. So we have to run the `generate-server-logs.py` manually. Here, as we are passing "output-logs" as the name of the output directory, we will be able to check all generated metrics there. We pass as well the process ID of the QUIC server because Mininet hosts are not isolated environments.
```
h2 python3 ../generate-server-logs.py -o output-logs -p \"$(jobs -l)\" &
```

It is a little difficult to simulate an attack manually, as we will have to keep sending requests which means we have to keep running the following command manually:

```
h1 python3 ../quic-src/send.py --ca-certs ../quic-src/tests/pycacert.pem https://10.0.2.2:4433/ &
```

###### We could use a for loop in the command line itself, but I couldn't make this work:
```
h1 for i in {1..10}; do python3 ../quic-src/send.py --ca-certs ../quic-src/tests/pycacert.pem https://10.0.2.2:4433/ &; done
```

After all this, you should be able to see a new directory called `output-logs` with the generated content.

## Running a Test Case In a Automated Way

Enter in the experiment's directory:
```
cd QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck
```

There are a `python` script called `run.py` that runs all the steps seen previously. When running it, you must provide a few arguments:
* `-s` or `--burst-size` (integer): it is how many requests each burst in the attack will carry.
* `-c` or `--burst-count` (integer): it is how many bursts will happen in the attack.
* `-t` or `--burst-interval` (float): it is the time interval between the bursts, in seconds.
* `-o` or `--output-folder` (string): it is the name of the directory where the server's logs will be placed when generated (default is `server-logs`).

To simply run an attack scenario, run the command below, changing W, X, Y, and Z for the arguments you want to pass, according to the written above:
```
python3 run.py -s W -c X -t Y -o Z
```

This script will compiler the `p4` program, start the Mininet environment, run all the commands we first ran manually, exits the Mininet, and clean the environment. The `json` output files will be generated under the names `server-cpu.json` and `server-mem.json` in the directory `Z/sW-cX-tY_0`.

## Running a Test Suite In a Automated Way
So, we saw that running a test case (experiment) in the automated way is simple, but it can still be tough to run a lot of them, a test suite. We recommend using a `bash` script with all the commands for all the test cases you want to run. In this way, you can leave it running it in a standardized way and go grab a cup of coffee. You do not need to restrict this `bash` script to one of the four scenarios, you can run all of them together to generate the logs for you to analyze it later.

Below, a sample of how you can do it:

```bash
#!/bin/bash

PATH="/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl"
N_SUITES = 5

# Run 5 test suites
for i in `seq $N_SUITES`
do
  # Run 4 test cases in each test suite varying the burst size parameter and fixing burst count and time interval.
  for j in 2 4 8 16
  do
    # The test suites will be organized in different directories while each test case has its parameters informations used to identify the json file with the metrics.
    python3 $PATH/2-Endpoints/QUIC-flood/run.py -s $j -c 2 -t 1 -o $PATH/Logs-Graphs/2-Endpoints/QUIC-flood/test_0$i;

    python3 $PATH/2-Endpoints/QUIC-Tr4ck/run.py -s $j -c 2 -t 1 -o $PATH/Logs-Graphs/2-Endpoints/QUIC-Tr4ck/test_0$i;
done    
```

## Generating Charts for the 2-Host Topology Experiment
The automated way to generate basic charts are very similar to the automated way to run the test cases and the test suites, because there already a `python` script for it too.

Enter the directory where all charts-related content are:
```
cd QUIC-Tr4ck-Impl/Logs-Graphs/2-Endpoints
```
The script that generate the charts requires parameters too. They are:
* `-f` or `--flood`: to plot the QUIC-flood metrics.
* `-k` or `--track`: to plot the QUIC-Tr4ck metrics.
* `-i` or `--input-files` (string): which files it will get the metrics from.
* `-r` or `--resource` (string): which measured resource is the plot about (you must pass one of the two options: `mem` or `cpu`. The default option is `mem`).
* `-a` or `--attribute` (string): which attribute of the resource is the plot about (default is `percent`).
* `-o` or `--output-file` (string): the name of the generated chart.
* `-d` or `--output-directory` (string): the name of the directory where the server's logs will be placed when generated (default is `output-folder`).
* `-x` or `--xlim` (float): the limits of the plot in axis X.
* `-y` or `--ylim` (float): the limits of the plot in axis Y.

Given this cheat sheet about the parameters of the generating chart script, you can use the script like this:

```
python3 ./generate-graphs.py -f -k -o s4-c8-t1_0 -i test_01/s4-c8-t1_0 -d vms-charts2 -a vms -y 30 70 -x 0 70;
```
