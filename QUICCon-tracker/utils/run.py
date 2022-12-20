import pexpect
import psutil
import argparse

# TODO:
# 1. chamar os scripts de cada endpoint
# 2. fazer um menu para rodar cliente, ataque, com mitigacao ou sem mitigacao
# 3. no script do ataque criar uma variavel de ambiente que sinaliza que o ataque terminou
# 4. ler essa variavel nesse script para encerrar o gerador de logs do servidor

class MininetProc:
    def __init__(self):
        proc = pexpect.spawn("make run", encoding="utf-8")
        proc.logfile = sys.stout
        proc.expect("mininet> ")

    def run_server(self):
        proc.sendline("h2 ./receive.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem")

    def run_server_logs(self):
        proc.sendline("h2 ./generate-logs-server.py")

    def stop_server_logs(self):
        # todo

    def run_client(self):
        proc.sendline("h1 ./send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/")

    def run_attack(self):
        proc.sendline("h1 ./attack.sh")


def main():
    clean()
    mininet_proc = MininetProc()
    mininet_proc.run_server()
    mininet_proc.run_attack()
