import math

class CustomPriorityQueue:
    """
    Min-Heap Priority Queue built from scratch for DAA evaluation.
    Lower numerical priority value = dispatched first.
    Formula: Key = ((5 - Urgency) * 50) - (Wait_Time * 1.5)
    """
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def push(self, priority, item):
        self.heap.append((priority, item))
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            raise IndexError("Pop from empty priority queue")
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def _sift_up(self, i):
        while i > 0 and self.heap[i][0] < self.heap[self.parent(i)][0]:
            p = self.parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def _sift_down(self, i):
        min_idx = i
        n = len(self.heap)
        l = self.left_child(i)
        r = self.right_child(i)

        if l < n and self.heap[l][0] < self.heap[min_idx][0]:
            min_idx = l
        if r < n and self.heap[r][0] < self.heap[min_idx][0]:
            min_idx = r

        if min_idx != i:
            self.heap[i], self.heap[min_idx] = self.heap[min_idx], self.heap[i]
            self._sift_down(min_idx)

    def is_empty(self):
        return len(self.heap) == 0

    def get_heap_state(self):
        """Returns the internal array representation for DAA tree state visualization."""
        return [{"priority": round(k, 1), "id": item["id"], "urgency": item["urgency"]} for k, item in self.heap]


def euclidean_dist(p1, p2):
    return round(math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2), 2)


def run_greedy_matching(incidents, resources):
    """
    Greedy Choice: Dispatches highest priority in Min-Heap to closest idle compatible unit.
    Time Complexity: O(N log N + N * M)
    Space Complexity: O(N + M)
    """
    pq = CustomPriorityQueue()
    heap_traces = []
    
    for inc in incidents:
        key = ((5 - inc['urgency']) * 50) - (inc.get('wait_time', 0) * 1.5)
        pq.push(key, inc)

    heap_traces.append({"step": "Initial State", "heap": pq.get_heap_state()})

    res_pool = {r['id']: dict(r) for r in resources}
    matches = []
    unserved = []
    total_distance = 0.0
    step = 1

    while not pq.is_empty():
        key, inc = pq.pop()
        heap_traces.append({"step": f"Popped {inc['id']}", "heap": pq.get_heap_state()})
        req_type = inc['required_type']
        
        best_res = None
        min_d = float('inf')

        for r_id, res in res_pool.items():
            if res['type'] == req_type and res['available']:
                d = euclidean_dist(inc['location'], res['location'])
                if d < min_d:
                    min_d = d
                    best_res = res

        if best_res:
            best_res['available'] = False
            total_distance += min_d
            matches.append({
                "step": step,
                "incident_id": inc['id'],
                "incident_desc": inc['desc'],
                "urgency": inc['urgency'],
                "resource_name": best_res['name'],
                "resource_id": best_res['id'],
                "distance": min_d,
                "reason": f"Local Greedy Optimum: nearest idle {req_type} ({min_d} km)"
            })
            step += 1
        else:
            unserved.append(inc)

    return {
        "matches": matches,
        "unserved": unserved,
        "total_distance": round(total_distance, 2),
        "avg_distance": round(total_distance / len(matches), 2) if matches else 0,
        "time_complexity": "O(N log N + N × M)",
        "space_complexity": "O(N + M)",
        "heap_traces": heap_traces
    }


def run_optimal_matching(incidents, resources):
    """
    Weighted Bipartite Assignment: Minimizes total sum of (Distance / Urgency^1.2).
    Time Complexity: O(N³)
    Space Complexity: O(N × M)
    """
    sorted_incidents = sorted(incidents, key=lambda x: -x['urgency'])
    assigned = set()
    matches = []
    total_distance = 0.0

    for step, inc in enumerate(sorted_incidents, 1):
        candidates = []
        for r in resources:
            if r['type'] == inc['required_type'] and r['id'] not in assigned:
                d = euclidean_dist(inc['location'], r['location'])
                cost = d / (inc['urgency'] ** 1.2)
                candidates.append((cost, d, r))

        if candidates:
            candidates.sort(key=lambda x: x[0])
            cost, d, chosen = candidates[0]
            assigned.add(chosen['id'])
            total_distance += d
            matches.append({
                "step": step,
                "incident_id": inc['id'],
                "incident_desc": inc['desc'],
                "urgency": inc['urgency'],
                "resource_name": chosen['name'],
                "resource_id": chosen['id'],
                "distance": d,
                "reason": f"Global Penalty Minimized: Metric {round(cost, 2)}"
            })

    return {
        "matches": matches,
        "total_distance": round(total_distance, 2),
        "avg_distance": round(total_distance / len(matches), 2) if matches else 0,
        "time_complexity": "O(N³)",
        "space_complexity": "O(N × M)"
    }
