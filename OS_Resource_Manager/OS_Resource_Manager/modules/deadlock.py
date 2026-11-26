def bankers(available, maximum, allocation):
    n = len(allocation)
    if n == 0 or len(maximum) != n:
        raise ValueError("Allocation and maximum matrices must have equal non-zero rows.")
    m = len(available)
    if any(len(row) != m for row in allocation + maximum):
        raise ValueError("Every matrix row must match the number of resource types.")
    if any(x < 0 for x in available):
        raise ValueError("Available resources cannot be negative.")
    need = []
    for i in range(n):
        row = []
        for j in range(m):
            if maximum[i][j] < allocation[i][j]:
                raise ValueError("Maximum demand cannot be less than current allocation.")
            row.append(maximum[i][j] - allocation[i][j])
        need.append(row)
    work = available[:]
    finish = [False] * n
    sequence = []
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                sequence.append(f"P{i}")
                changed = True
    return {"safe": all(finish), "sequence": sequence, "need": need}

def run_deadlock_menu():
    available = [3,3,2]
    maximum = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
    allocation = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
    result = bankers(available, maximum, allocation)
    print("Banker's Algorithm:", "SAFE" if result["safe"] else "UNSAFE")
    print("Safe sequence:", " -> ".join(result["sequence"]) if result["safe"] else "No complete safe sequence")
