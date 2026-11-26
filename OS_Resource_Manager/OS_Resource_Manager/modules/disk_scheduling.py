def _validate(requests, head, disk_size):
    if disk_size <= 0 or not 0 <= head < disk_size:
        raise ValueError("Disk size must be positive and head must be within disk bounds.")
    if any(r < 0 or r >= disk_size for r in requests):
        raise ValueError("Every disk request must be within disk bounds.")

def fcfs(requests, head, disk_size=200):
    _validate(requests, head, disk_size)
    order = [head] + list(requests)
    return {"order": order, "movement": sum(abs(b-a) for a,b in zip(order,order[1:]))}

def sstf(requests, head, disk_size=200):
    _validate(requests, head, disk_size)
    pending, order, current = list(requests), [head], head
    while pending:
        nxt = min(pending, key=lambda x: (abs(x-current), x))
        pending.remove(nxt); order.append(nxt); current = nxt
    return {"order": order, "movement": sum(abs(b-a) for a,b in zip(order,order[1:]))}

def scan(requests, head, disk_size=200, direction="right"):
    _validate(requests, head, disk_size)
    if direction not in ("right","left"):
        raise ValueError("Direction must be 'right' or 'left'.")
    left = sorted([r for r in requests if r < head], reverse=True)
    right = sorted(r for r in requests if r >= head)
    if direction == "right":
        order = [head] + right
        if (not order or order[-1] != disk_size-1) and left:
            order.append(disk_size-1)
        order += left
    else:
        order = [head] + left
        if order[-1] != 0 and right:
            order.append(0)
        order += right
    return {"order": order, "movement": sum(abs(b-a) for a,b in zip(order,order[1:]))}

def run_disk_menu():
    requests, head = [98,183,37,122,14,124,65,67], 53
    for name, fn in [("FCFS",fcfs),("SSTF",sstf),("SCAN",scan)]:
        r = fn(requests, head)
        print(f"{name:6} total head movement={r['movement']} cylinders; order={r['order']}")
