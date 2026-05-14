# The Torchbearer

**Student Name:** Daud Abdinasir
**Student ID:** 129393274
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  _Dijkstra explores from S an least-cost path tree that finds minimum costs to each node‚ but it does not determine the order in which to visit the relic chambers․_

- **What decision remains after all inter-location costs are known:**
  _What is the cheapest ordering of the relic chambers so that traveling from S through each relic to T is cheapest?_

- **Why this requires a search over orders (one sentence):**
  _This also means that the optimal route is a global property of the ordering of the nodes to be visited‚ rather than a local property․_

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type             | Why it is a source                                                                              |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| Spawn (S)                    | The Torchbearer departs from S first, so we need cheapest paths from S to every relic and to T. |
| Each relic chamber (R1...Rk) | After visiting a relic, the Torchbearer departs from it to the next relic or to T.              |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property                    | Your answer                                                                           |
| --------------------------- | ------------------------------------------------------------------------------------- |
| Data structure name         | Nested dictionary (`dict[node, dict[node, float]]`)                                   |
| What the keys represent     | Source node — the location the Torchbearer is departing from                          |
| What the values represent   | A dictionary mapping every destination node to its minimum fuel cost from that source |
| Lookup time complexity      | O(1)                                                                                  |
| Why O(1) lookup is possible | Python dictionaries use hash tables; key lookup does not depend on number of entries  |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** k + 1 — one from spawn, one from each of the k relics
- **Cost per run:** O(m log n) where n = |V|, m = |E|
- **Total complexity:** O((k + 1) · m log n)
- **Justification (one line):** We run one full Dijkstra per source and there are exactly k + 1 sources — spawn plus each relic; exit node T is never a departure point.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  The final value of dist[v] will be the minimum-cost path from the source to v‚ and no relaxation can improve this distance․

- **For nodes not yet finalized (not in S):**
  dist[u] is the best guess of the cost of the path from the starting node to u using only finalized nodes in the path‚ although this cost may still decrease․

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  S is empty‚ dist[source] is 0‚ and all other distances are initialized to infinity․ In particular‚ the invariant is trivially true because no vertices are finalized: any non-finalized distance is the shortest path with no internal vertices in S․

- **Maintenance : why finalizing the min-dist node is always correct:**
  By processing the node u with the smallest value of dist[u] and then finalizing it‚ and because all edge weights are nonnegative‚ we cannot reach u from an unfinalized node at a lower cost‚ since any detour would have added nonnegative cost to that of the shortest path․

- **Termination : what the invariant guarantees when the algorithm ends:**
  Every reachable node is in S‚ and its weight is correctly defined as its shortest-path distance from the source․ Unreachable nodes all have dist = infinity․

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

## Choosing an entry in dist_table that is incorrect might select a false minimum cost ordering in dist_table‚ causing extra distance to be traversed or rendering the ordering impossible․ For example‚ on a false minimum minimum ordering the Torchbearer could waste torch fuel‚ or not reach the exit․

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** Unlike a greedy approach (which goes directly to the closest unvisited relic)‚ the construction search minimizes the next step's cost to the closest relic․
- **Counter-example setup:** The‌ shortest path between S and T‚ if the relics are in the vertices B‚ C‚ D‚ satisfies the required distances: dist(S‚B)=1‚ dist(S‚C)=2‚ dist(S‚D)=2‚ dist(B‚D)=1‚ dist(B‚T)=1‚ dist(C‚B)=1‚ dist(C‚T)=1‚ dist(D‚B)=1 and dist(D‚C)=1․
- **What greedy picks:** S leads to B (1‚ the closest)‚ then to D (1)‚ then to C (1)‚‌ then to T (1)‚ for 4 total․
- **What optimal picks:** S → B → D → C → T = total 4․ If instead dist(B‚C) = 100‚ then greedy will pick B first (cost 1) and then be forced to pay 100 to reach C․ If we go to C first‚ we avoid this edge and the cost is 2․
- **Why greedy loses:** Greedy does not look ahead: it will on each move choose the cheapest option‚ without knowing whether this will lead to an expensive future leg.

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- The algorithm must cover every possible order of visiting the relic chambers‚ extending the best complete route found thus far if necessary and pruning infeasible branches of the route tree․

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component                | Variable name in code | Data type      | Description                                                                         |
| ------------------------ | --------------------- | -------------- | ----------------------------------------------------------------------------------- |
| Current location         | `current_loc`         | node (str/int) | The node the Torchbearer is currently at                                            |
| Relics already collected | `relics_remaining`    | `set`          | The set of relics not yet visited — a relic is collected when removed from this set |
| Fuel cost so far         | `cost_so_far`         | `float`        | Accumulated fuel spent from spawn to current location                               |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property                                    | Your answer                                                                                                       |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Data structure chosen                       | `set`                                                                                                             |
| Operation: check if relic already collected | Time complexity: O(1)                                                                                             |
| Operation: mark a relic as collected        | Time complexity: O(1) — `relics_remaining.remove(relic)`                                                          |
| Operation: unmark a relic (backtrack)       | Time complexity: O(1) — `relics_remaining.add(relic)`                                                             |
| Why this structure fits                     | All three operations are O(1) via hashing, making backtracking cheap and membership checks during pruning instant |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** k! where k = |M|
- **Why:** Without pruning‚ at each step‚ the algorithm can branch on each remaining relic‚ so the search space has a branching factor of k · (k−1) · ․․․ · 1․

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** `best[0]` keeps track of the full fuel cost of the cheapest valid route found so far‚ and `best[1]` stores the order of the relics in that route․
- **What the lower bound accounts for:** At every recursive call‚ we compare cost_so_far + an estimate of the remaining cost to best[0]․
- **Why it never overestimates:** Any branch where the partial cost is equal to or greater than best[0] is discarded because no complete route down that branch can improve the current best․

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- If cost_so_far + lower_bound >= best[0] then all complete routes from this state have cost greater than or equal to best[0]․
- Hence we are safe in pruning this branch‚ since the optimal solution would either have already been encountered (and so recorded)‚ or it would not travel through this state․

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
