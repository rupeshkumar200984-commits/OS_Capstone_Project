def allocate(blocks, processes, strategy):
    if any(b <= 0 for b in blocks) or any(p <= 0 for p in processes):
        raise ValueError("Memory blocks and process sizes must be positive.")
    remaining = list(blocks)
    allocations, internal_frag = [], []
    for size in processes:
        candidates = [i for i, free in enumerate(remaining) if free >= size]
        if not candidates:
            allocations.append(None); internal_frag.append(0); continue
        if strategy == "first":
            idx = candidates[0]
        elif strategy == "best":
            idx = min(candidates, key=lambda i: remaining[i])
        elif strategy == "worst":
            idx = max(candidates, key=lambda i: remaining[i])
        else:
            raise ValueError("Unknown allocation strategy.")
        internal_frag.append(remaining[idx] - size)
        allocations.append(idx)
        remaining[idx] = 0  # fixed partition: block is assigned to one process
    return {"allocations": allocations, "remaining_blocks": remaining,
            "internal_fragmentation": sum(internal_frag),
            "allocated_count": sum(x is not None for x in allocations),
            "process_count": len(processes)}

def run_memory_menu():
    blocks, processes = [100,500,200,300,600], [212,417,112,426]
    for strategy in ("first","best","worst"):
        r = allocate(blocks, processes, strategy)
        print(f"{strategy.title()} Fit: {r['allocated_count']}/{r['process_count']} allocated; "
              f"internal fragmentation={r['internal_fragmentation']} KB")
