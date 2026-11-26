import unittest
from modules.cpu_scheduling import fcfs, sjf_non_preemptive, round_robin
from modules.memory_management import allocate
from modules.deadlock import bankers
from modules.disk_scheduling import fcfs as disk_fcfs, sstf

class TestOSAlgorithms(unittest.TestCase):
    def setUp(self):
        self.processes = [
            {"pid":"P1","arrival":0,"burst":5,"priority":2},
            {"pid":"P2","arrival":1,"burst":3,"priority":1},
        ]

    def test_cpu_fcfs_metrics(self):
        result = fcfs(self.processes)
        self.assertEqual(result["avg_waiting"], 2.0)
        self.assertEqual(result["avg_turnaround"], 6.0)

    def test_sjf_completes_all(self):
        result = sjf_non_preemptive(self.processes)
        self.assertEqual(len(result["rows"]), 2)

    def test_round_robin_completes_all(self):
        result = round_robin(self.processes, 2)
        self.assertEqual(len(result["rows"]), 2)

    def test_memory_best_fit(self):
        result = allocate([100, 500, 200], [180], "best")
        self.assertEqual(result["allocations"], [2])

    def test_bankers_safe(self):
        result = bankers([3,3,2],
            [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]],
            [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]])
        self.assertTrue(result["safe"])

    def test_disk_movement(self):
        result = disk_fcfs([10,20], 5, 100)
        self.assertEqual(result["movement"], 15)

    def test_invalid_burst_rejected(self):
        with self.assertRaises(ValueError):
            fcfs([{"pid":"P1","arrival":0,"burst":0}])

if __name__ == "__main__":
    unittest.main()
