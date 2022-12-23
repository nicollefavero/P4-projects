while true
do
   sudo seq 1 100 | timeout 5s xargs -n1 -P100 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/
done
