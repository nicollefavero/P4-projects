import psutil
import datetime

with open("logs/server-memory.txt", "a") as m:
    with open("logs/server-cpu.txt", "a") as c:
        
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percen()

        m.write(f"[{datetime.now()}] {mem}")
        c.write(f"[{datetime.now()}] CPU percent: {cpu}")
