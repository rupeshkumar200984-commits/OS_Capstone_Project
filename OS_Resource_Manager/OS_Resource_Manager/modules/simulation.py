from datetime import datetime
from pathlib import Path
import logging

from modules.cpu_scheduling import fcfs, sjf_non_preemptive, priority_non_preemptive, round_robin
from modules.memory_management import allocate
from modules.deadlock import bankers
from modules.disk_scheduling import fcfs as disk_fcfs, sstf, scan
from modules.analytics import (save_cpu_report, save_memory_report, save_disk_report,
                               save_deadlock_report, save_chart)

def _print_table(title, headers, rows):
    print("\n" + title)
    widths = [max(len(str(h)), *(len(str(row[i])) for row in rows)) for i,h in enumerate(headers)]
    line = "+-" + "-+-".join("-"*w for w in widths) + "-+"
    print(line)
    print("| " + " | ".join(str(h).ljust(widths[i]) for i,h in enumerate(headers)) + " |")
    print(line)
    for row in rows:
        print("| " + " | ".join(str(v).ljust(widths[i]) for i,v in enumerate(row)) + " |")
    print(line)

def run_complete_simulation():
    Path("reports").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(filename="logs/activity.log", level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s", force=True)
    logging.info("Complete simulation started")
    print("\n" + "="*62)
    print("             RUNNING COMPLETE OS SIMULATION")
    print("="*62)

    # One shared, documented sample dataset per resource domain.
    processes = [
        {"pid":"P1","arrival":0,"burst":5,"priority":2},
        {"pid":"P2","arrival":1,"burst":3,"priority":1},
        {"pid":"P3","arrival":2,"burst":8,"priority":3},
        {"pid":"P4","arrival":3,"burst":2,"priority":2},
    ]
    cpu = {
        "FCFS": fcfs(processes),
        "SJF (non-preemptive)": sjf_non_preemptive(processes),
        "Priority (non-preemptive)": priority_non_preemptive(processes),
        "Round Robin (q=2)": round_robin(processes, quantum=2),
    }
    cpu_rows = [(name, f"{r['avg_waiting']:.2f}", f"{r['avg_turnaround']:.2f}") for name,r in cpu.items()]
    _print_table("1) CPU SCHEDULING", ["Algorithm","Avg waiting","Avg turnaround"], cpu_rows)
    print("FCFS Gantt timeline:", " | ".join(f"{p}[{s}-{e}]" for p,s,e in cpu["FCFS"]["timeline"]))

    blocks, process_sizes = [100,500,200,300,600], [212,417,112,426]
    memory = {name: allocate(blocks, process_sizes, key)
              for name,key in [("First Fit","first"),("Best Fit","best"),("Worst Fit","worst")]}
    memory_rows = [(name, f"{r['allocated_count']}/{r['process_count']}", r["internal_fragmentation"])
                   for name,r in memory.items()]
    _print_table("2) MEMORY ALLOCATION (fixed partitions)", ["Algorithm","Allocated","Internal frag. (KB)"], memory_rows)

    available = [3,3,2]
    maximum = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
    allocation = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
    deadlock = bankers(available, maximum, allocation)
    print("\n3) DEADLOCK / BANKER'S ALGORITHM")
    print("System state:", "SAFE" if deadlock["safe"] else "UNSAFE")
    print("Safe sequence:", " -> ".join(deadlock["sequence"]) if deadlock["safe"] else "No complete safe sequence")

    requests, head, disk_size = [98,183,37,122,14,124,65,67], 53, 200
    disk = {"FCFS": disk_fcfs(requests,head,disk_size),
            "SSTF": sstf(requests,head,disk_size),
            "SCAN (right)": scan(requests,head,disk_size,"right")}
    disk_rows = [(name,r["movement"], " -> ".join(map(str,r["order"]))) for name,r in disk.items()]
    _print_table("4) DISK SCHEDULING", ["Algorithm","Head movement","Service order"], disk_rows)

    save_cpu_report(cpu)
    save_memory_report(memory)
    save_deadlock_report(deadlock)
    save_disk_report(disk)
    chart_created = save_chart(cpu, disk)
    logging.info("Complete simulation finished successfully")
    print("\n5) REPORTS")
    print("CSV reports saved in ./reports/")
    print("Activity log saved in ./logs/activity.log")
    print("Charts:", "created" if chart_created else "not created (install matplotlib to enable charts)")
    print("\nSimulation completed successfully.")
    print("Sample datasets are embedded in modules/simulation.py; edit them to run your own scenarios.")
