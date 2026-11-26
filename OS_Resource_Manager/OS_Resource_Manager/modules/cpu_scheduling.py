def _validate_processes(processes):
    if not processes:
        raise ValueError("At least one process is required.")
    ids = set()
    for p in processes:
        if p["pid"] in ids:
            raise ValueError(f"Duplicate process ID: {p['pid']}")
        ids.add(p["pid"])
        if p["arrival"] < 0 or p["burst"] <= 0:
            raise ValueError("Arrival time must be >= 0 and burst time must be > 0.")
        if p.get("priority", 1) < 0:
            raise ValueError("Priority must be >= 0.")

def _metrics(processes, completion, timeline):
    rows = []
    for p in processes:
        ct = completion[p["pid"]]
        tat = ct - p["arrival"]
        wt = tat - p["burst"]
        rows.append({"pid": p["pid"], "arrival": p["arrival"], "burst": p["burst"],
                     "completion": ct, "turnaround": tat, "waiting": wt})
    n = len(rows)
    return {"rows": rows, "avg_waiting": sum(x["waiting"] for x in rows)/n,
            "avg_turnaround": sum(x["turnaround"] for x in rows)/n, "timeline": timeline}

def fcfs(processes):
    _validate_processes(processes)
    ordered = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))
    t, completion, timeline = 0, {}, []
    for p in ordered:
        start = max(t, p["arrival"])
        if start > t:
            timeline.append(("IDLE", t, start))
        end = start + p["burst"]
        timeline.append((p["pid"], start, end))
        completion[p["pid"]] = end
        t = end
    return _metrics(processes, completion, timeline)

def sjf_non_preemptive(processes):
    _validate_processes(processes)
    pending = list(processes)
    t, completion, timeline = 0, {}, []
    while pending:
        ready = [p for p in pending if p["arrival"] <= t]
        if not ready:
            next_arrival = min(p["arrival"] for p in pending)
            timeline.append(("IDLE", t, next_arrival))
            t = next_arrival
            continue
        p = min(ready, key=lambda x: (x["burst"], x["arrival"], x["pid"]))
        pending.remove(p)
        end = t + p["burst"]
        timeline.append((p["pid"], t, end))
        completion[p["pid"]] = end
        t = end
    return _metrics(processes, completion, timeline)

def priority_non_preemptive(processes):
    _validate_processes(processes)
    pending = list(processes)
    t, completion, timeline = 0, {}, []
    while pending:
        ready = [p for p in pending if p["arrival"] <= t]
        if not ready:
            nxt = min(p["arrival"] for p in pending)
            timeline.append(("IDLE", t, nxt))
            t = nxt
            continue
        p = min(ready, key=lambda x: (x.get("priority", 1), x["arrival"], x["pid"]))
        pending.remove(p)
        end = t + p["burst"]
        timeline.append((p["pid"], t, end))
        completion[p["pid"]] = end
        t = end
    return _metrics(processes, completion, timeline)

def round_robin(processes, quantum=2):
    _validate_processes(processes)
    if quantum <= 0:
        raise ValueError("Time quantum must be > 0.")
    pending = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))
    remaining = {p["pid"]: p["burst"] for p in processes}
    completion, timeline = {}, []
    ready, t, i = [], 0, 0
    while len(completion) < len(processes):
        while i < len(pending) and pending[i]["arrival"] <= t:
            ready.append(pending[i]); i += 1
        if not ready:
            if i < len(pending):
                nxt = pending[i]["arrival"]
                timeline.append(("IDLE", t, nxt)); t = nxt
                continue
            break
        p = ready.pop(0)
        run = min(quantum, remaining[p["pid"]])
        start = t
        t += run
        remaining[p["pid"]] -= run
        timeline.append((p["pid"], start, t))
        while i < len(pending) and pending[i]["arrival"] <= t:
            ready.append(pending[i]); i += 1
        if remaining[p["pid"]] > 0:
            ready.append(p)
        else:
            completion[p["pid"]] = t
    return _metrics(processes, completion, timeline)

def run_cpu_menu():
    sample = [
        {"pid":"P1","arrival":0,"burst":5,"priority":2},
        {"pid":"P2","arrival":1,"burst":3,"priority":1},
        {"pid":"P3","arrival":2,"burst":8,"priority":3},
        {"pid":"P4","arrival":3,"burst":2,"priority":2},
    ]
    print("\nCPU scheduling demo dataset:", sample)
    for name, fn in [("FCFS",fcfs),("SJF",sjf_non_preemptive),
                     ("Priority",priority_non_preemptive),
                     ("Round Robin",lambda x: round_robin(x,2))]:
        r = fn(sample)
        print(f"{name:12} Avg waiting={r['avg_waiting']:.2f}, Avg turnaround={r['avg_turnaround']:.2f}")
