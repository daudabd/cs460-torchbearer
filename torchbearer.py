"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: ___________________________
Student ID:   ___________________________

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return (
        "- Although one run of the single-source shortest-path algorithm from S gives the minimum prices to each of the nodes "
        "it does not give the optimal ORDER in which to visit the relic chambers․ "
        "Dijkstra's algorithm does not give any method for comparing permutations․\n\n"
        "- Once all the inter-location travel costs have been computed "
        "the only remaining design decision is that of the ordering of the relic chambers "
        "that minimizes the total fuel cost of traveling from S through all the relic chambers to T․\n\n"
        "- Solving this ordering problem requires searching "
        "all possible orderings or pruning large numbers of them․"
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """
    sources = set()
    sources.add(spawn)
    for r in relics:
        sources.add(r)
    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]:
            continue
        for v, weight in graph[u]:
            new_cost = dist[u] + weight
            if new_cost < dist[v]:
                dist[v] = new_cost
                heapq.heappush(heap, (new_cost, v))
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    TODO
    """
    return "Part 3a: After S is finalized‚ dist[v] is the true minimum-cost"
    "path from s to v after S․ Since no other node can be added to S‚"
    "dist[v] cannot be improved․ Before S is finalized‚"
    "dist[u] is the best-known target distance with only finalized nodes used as intermediate nodes․"
    "This is a loose upper bound that can be improved․ \n\n" 
    "Part 3b: Initialization vacuously holds as S is empty and dist[source]=0 while others are infinities․"
    "Maintenance holds since u‚ the min-dist node‚ has been finalized‚"
    "and no nonnegative edge can lead to a reduction of dist[u] via nonfinalized nodes․"
    "Termination: every reachable node has its true shortest distance confirmed․ \n\n"  
    "Part 3c: The planner picks some ordering of relics that appears to be" 
    "the cheapest according to the dist_table but costs more or is impossible in the real dungeon․"


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    return "Why Greedy Fails: Greedy always chooses the closest unvisited relic‚" 
    "a local-minimum heuristic‚ while the optimal solution might just have to take a much bigger step․" 
    "For example‚ assume dist(S‚B)=1‚ dist(B‚C)=100‚ dist(S‚C)=2‚ dist(C‚B)=1․" 
    "Greedy visits B with cost 1+100=101․ The optimal solution visits C and B in that order with cost 2+1=3․" 
    "Greedy fails because a low-cost first leg can lead to high-cost latter legs after a few․"
    "What the Algorithm Must Explore: all orders of visiting the relic chambers‚" 
    "pruning branches that cannot beat the current best solution․"


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    best = [float('inf'), []]
    relics_remaining = set(relics)
    relics_visited_order = []
    _explore(dist_table, spawn, relics_remaining, relics_visited_order,
             0.0, exit_node, best)
    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    # Lower-bound pruning: the cheapest possible next leg gives a lower
    # bound on remaining cost. If cost_so_far + that bound already meets
    # or exceeds best[0], no complete route from this state can improve it.
    if relics_remaining:
        sources = dist_table.get(current_loc, {})
        min_next = min(sources.get(r, float('inf')) for r in relics_remaining)
        # PRUNING SAFETY: This lower bound only charges for one mandatory leg
        # and ignores all subsequent legs, so it never overestimates remaining
        # cost. Any complete route from here costs at least cost_so_far +
        # min_next, so pruning when that meets or exceeds best[0] is safe.
        if cost_so_far + min_next >= best[0]:
            return

    if not relics_remaining:
        cost_to_exit = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        total_cost = cost_so_far + cost_to_exit
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)
        return

    for relic in list(relics_remaining):
        travel_cost = dist_table.get(current_loc, {}).get(relic, float('inf'))
        if travel_cost == float('inf'):
            continue
        new_cost = cost_so_far + travel_cost
        if new_cost >= best[0]:
            continue
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
        _explore(dist_table, relic, relics_remaining, relics_visited_order,
                 new_cost, exit_node, best)
        relics_remaining.add(relic)
        relics_visited_order.pop()


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
