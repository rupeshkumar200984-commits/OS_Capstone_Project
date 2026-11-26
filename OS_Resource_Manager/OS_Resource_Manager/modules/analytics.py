import csv
from pathlib import Path

REPORT_DIR = Path("reports")

def write_csv(path, headers, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def save_cpu_report(results):
    rows = []
    for algorithm, result in results.items():
        rows.append({"algorithm": algorithm, "average_waiting": round(result["avg_waiting"], 2),
                     "average_turnaround": round(result["avg_turnaround"], 2)})
    write_csv(REPORT_DIR / "cpu_comparison.csv",
              ["algorithm","average_waiting","average_turnaround"], rows)

def save_memory_report(results):
    rows = [{"algorithm": k, "allocated_processes": v["allocated_count"],
             "total_processes": v["process_count"],
             "internal_fragmentation_kb": v["internal_fragmentation"]}
            for k,v in results.items()]
    write_csv(REPORT_DIR / "memory_comparison.csv",
              ["algorithm","allocated_processes","total_processes","internal_fragmentation_kb"], rows)

def save_disk_report(results):
    rows = [{"algorithm": k, "total_head_movement": v["movement"],
             "service_order": " -> ".join(map(str,v["order"]))} for k,v in results.items()]
    write_csv(REPORT_DIR / "disk_comparison.csv",
              ["algorithm","total_head_movement","service_order"], rows)

def save_deadlock_report(result):
    write_csv(REPORT_DIR / "deadlock_report.csv", ["safe","safe_sequence"],
              [{"safe": result["safe"], "safe_sequence": " -> ".join(result["sequence"])}])

def save_chart(cpu_results, disk_results):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        names = list(cpu_results)
        waits = [cpu_results[n]["avg_waiting"] for n in names]
        plt.figure(figsize=(8,4.5))
        plt.bar(names, waits)
        plt.ylabel("Average waiting time (time units)")
        plt.title("CPU Scheduling: Average Waiting Time")
        plt.tight_layout()
        plt.savefig(REPORT_DIR / "cpu_waiting_comparison.png", dpi=150)
        plt.close()

        names = list(disk_results)
        movement = [disk_results[n]["movement"] for n in names]
        plt.figure(figsize=(7,4.5))
        plt.bar(names, movement)
        plt.ylabel("Total head movement (cylinders)")
        plt.title("Disk Scheduling: Total Head Movement")
        plt.tight_layout()
        plt.savefig(REPORT_DIR / "disk_movement_comparison.png", dpi=150)
        plt.close()
        return True
    except ImportError:
        return False

def show_latest_reports():
    report_dir = Path("reports")
    if not report_dir.exists() or not list(report_dir.glob("*.csv")):
        print("No reports found. Run option 6 first.")
        return
    print("\nAvailable reports:")
    for p in sorted(report_dir.iterdir()):
        if p.is_file():
            print(f" - {p}")
