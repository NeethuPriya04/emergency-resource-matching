# Problem 90: Emergency Resource Matching Optimization Engine

---

## 1. Executive Summary

The Emergency Resource Matching System is an algorithmic dispatch optimization engine designed to pair high-stress incidents with emergency vehicles in real time. Standard First-In-First-Out (FIFO) queuing fails in emergency services because critical calls wait behind non-critical calls and vehicle routing becomes inefficient.

This prototype models and solves dispatch constraints using core Data Analysis and Algorithms (DAA) concepts:
- Urgency Levels (1 to 4): Life-threatening calls preempt lower-priority tasks.
- Resource Suitability: Incidents only receive compatible units (Ambulance, Fire Tender, Police Patrol).
- Spatial Proximity: Euclidean distance is minimized to reduce response times.

---

## 2. Algorithmic Architecture

### A. Custom Binary Min-Heap (Priority Queue)
Implemented from scratch using array indexing to demonstrate fundamental heap invariants:
- Parent Index: (i - 1) // 2
- Left Child Index: 2 * i + 1
- Right Child Index: 2 * i + 2
- Priority Key Formula:
  Priority Key = ((5 - Urgency) * 50) - (Wait Time * 1.5)
  Level 4 urgency produces the lowest numerical value, surfacing immediately at the heap root. The wait-time factor dynamically reduces the key as calls wait, preventing starvation of minor incidents.
- Complexity: Insertion (push with Sift-Up) runs in O(log N); Extraction (pop with Sift-Down) runs in O(log N).

### B. Algorithm 1: Greedy Dispatch Heuristic (Local Optimum)
- Strategy: Continuously pops the root incident from the Min-Heap and assigns the closest available, type-compatible vehicle.
- Time Complexity: O(N log N + N * M)
- Space Complexity: O(N + M)
- Trade-off: Delivers sub-millisecond real-time dispatch decisions.

### C. Algorithm 2: Global Optimal Bipartite Matching (Global Optimum)
- Strategy: Solves an assignment matrix to minimize total city-wide penalty:
  Minimize Sum of (Distance / (Urgency ^ 1.2))
- Time Complexity: O(N^3)
- Space Complexity: O(N * M)
- Trade-off: Produces the lowest overall travel distance, but requires global matrix recomputation.

---

## 3. Algorithm Complexity and Performance Benchmark

| Metric | Greedy + Min-Heap | Global Optimal (Bipartite) |
| :--- | :--- | :--- |
| Optimization Target | Immediate local response latency | System-wide global cost minimization |
| Time Complexity | O(N log N + N * M) | O(N^3) |
| Space Complexity | O(N + M) | O(N * M) |
| Scalability | Extremely High (Real-time sub-millisecond) | Moderate (Matrix permutation overhead) |
| Starvation Handling | Dynamic wait-time aging penalty | Cost function weighting |
| Backtracking | None (Immediate local choice) | Global combinatorial assignment |

---

## 4. Repository Structure

```text
emergency-resource-matching/
|-- algorithms.py          # Custom Min-Heap, Greedy & Bipartite implementations
|-- app.py                 # Flask REST server and API routes
|-- requirements.txt       # Python package requirements
|-- README.md              # Complete technical documentation
|-- Presentation.pptx      # Viva presentation slide deck
|-- static/
|   |-- app.js             # Canvas coordinate map and API trigger
|   `-- style.css          # Clean dashboard styling
`-- templates/
    `-- index.html         # Prototype interface and trace table
