# OS Resource Manager

A menu-driven Python + Bash operating-system resource-management simulator.

## Features
- CPU scheduling: FCFS, non-preemptive SJF, non-preemptive Priority, Round Robin.
- Memory allocation: First Fit, Best Fit, Worst Fit (fixed partitions).
- Deadlock safety: Banker's Algorithm.
- Disk scheduling: FCFS, SSTF, SCAN.
- Complete simulation (menu option 6): runs all modules on reproducible sample datasets, prints comparison tables, exports CSV reports, creates charts when Matplotlib is installed, and writes activity logs.

## Requirements
- Python 3.9+
- Bash (Linux, macOS, or WSL on Windows)
- Matplotlib for charts (optional; CSV reports work without it)

## Run
```bash
chmod +x launcher.sh
./launcher.sh
```

Alternatively:
```bash
python3 main.py
```

Choose `6` for Run Complete Simulation.

## Generated outputs
- `reports/cpu_comparison.csv`
- `reports/memory_comparison.csv`
- `reports/deadlock_report.csv`
- `reports/disk_comparison.csv`
- `reports/cpu_waiting_comparison.png` (if Matplotlib is installed)
- `reports/disk_movement_comparison.png` (if Matplotlib is installed)
- `logs/activity.log`
- `logs/launcher.log`

## Algorithm assumptions
- SJF and Priority are non-preemptive. A lower numeric priority value means higher priority.
- Round Robin uses a time quantum of 2 in the complete simulation.
- Memory uses fixed partitions: an allocated block is reserved as a whole; the leftover space is counted as internal fragmentation.
- SCAN moves toward the right first and reaches the disk end when there are requests on the opposite side.
- The Banker's Algorithm sample is a standard five-process, three-resource safety example.

## Tests
```bash
python3 -m unittest discover -s tests -v
```
