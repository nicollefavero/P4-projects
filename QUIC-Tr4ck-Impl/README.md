# QUIC-Tr4ck

## How the Experiments Are Organized
There are two scenarios for the experiments: one with a topology of 2 end systems, and another with 3 end systems. In both experiments there are only one switch which all end systems are connected to. Each of these scenarios has two experiments: one without mitigation, just the QUIC flood attack, and another with the mitigation technique, the QUIC-Tr4ck.    

All four experiments have the same directory structure:   

* `p4-src`: where all `P4`-related files are.   
* `quic-src`: where all `aioquic`-related files are, such as the scripts that run the QUIC client and the QUIC server as well as its dependencies (cloned from `aioquic` repository).   
* `utils`: here are all sort of scripts necessary to create and run the environment that emulates the programmable switch (cloned from `p4-tutorial` repository).   
* There are also two `python` scripts in the same directory level as stuff listed above: `run.py` and `generate-server-logs.py`. These scripts' goal is to automate everything, from `mininet` instantiation to experiments running and environment cleaning, and also logging.    

## Running a Experiment Manually

For the explanation, I will be using `QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/` directory's content, but every step is reproducible within the other three experiments.   

Inside the folder `QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/p4-src`, there is a Makefile file that sets some variables and calls another Makefile in `QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/utils`. These Makefiles compile the P4 program `main.p4` and start the Mininet environment using all the configuration files from `p4-src/topology` and `utils`. But the commands are very simple:   

To enter the right directory:
```
cd QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/p4-src
```

To compile the P4 program and start the Mininet:
```
make run
```

After a lot of output in the terminal, you shall see the following line that expects you to enter more commands:
```
mininet>
```

To actually run the experiment, we must run the server in a non-blocking way inside the Mininet. We will run the server on host `h2`:
```
h2 python3 {absolute_path}/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/quic-src/receive.py --certificate {absolute_path}/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/quic-src/tests/ssl_cert.pem --private-key {absolute_path}/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/quic-src/tests/ssl_key.pem &
```

Right after running the server, we are interested in seeing some metrics and logs. So we have to run the `generate-server-logs.py` manually. Here, as we are passing "output-logs" as the name of the output directory, we will be able to check all generated metrics there. We pass as well the process ID of the QUIC server because Mininet hosts are not isolated environments.
```
h2 python3 {absolute_path}/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/generate-server-logs.py -o output-logs -p \"$(jobs -l)\" &
```

It is a little difficult to simulate an attack manually, as we will have to keep sending requests which means we have to keep running the following command:

```
h1 python3 {absolute_path}/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/quic-src/send.py --ca-certs {absolute_path}/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/quic-src/tests/pycacert.pem https://10.0.2.2:4433/ &
```


### How to Run a Experiment using `run.py` Script
