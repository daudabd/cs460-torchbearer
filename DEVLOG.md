# Development Log – The Torchbearer

**Student Name:** Daud Abdinasir\*\*
**Student ID:** 129393274\*\*

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [05/12/2026]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

Before typing any code‚ understand the specific problem: we want to visit
a set of relic chambers in a weighted directed graph with minimum fuel cost․
I plan to compute all-pairs shortest paths between all the important positions
using Dijkstra and then search all permutations of the relic chambers with
backtracking and pruning․ I suspect the most difficult part of making the
lower bound admissible without being too loose will be pruning in \_explore()․
I will run your provided \_run_tests() function and add more edge cases with unreachable nodes․

---

## Entry 2 – [05/12/2026]: [Wrong Assumption on Source Selection]

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

I initially thought that Dijkstra's had to be run from every node‚
instead of just the exit node T․ The Torchbearer only ever DEPARTS
from spawn chambers and relics‚ never from T‚ and T is only ever a destination node․
I had to fix select_sources() to iterate through spawn and relics‚ but not exit_node․
This also keeps the precomputation step efficient‚ as we do not need to run Dijkstra again․

---

## Entry 3 – [05/14/2026]: [Bug in Source Selection]

I thought I needed to run Dijkstra from all graph nodes including
exit node T but later realized T was only a destination as the
Torchbearer never left T․ Removing T from selected_sources() eliminated
the redundant second run and kept dist_table clean․
This assumption turned out wrong when caught early before causing routing issues․

---

## Entry 4 – [05/14/2026]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

This implementation passes the 5 tests provided․ Given more time‚
I would improve the lower bound of \_explore() from the cost of a
single next leg to the total cost of the tour including the cost
of getting to T․ This would prune many more branches‚ and the algorithm
would be more efficient for large relic sets․ I would also like to add
stress tests with 8+ relics‚ to measure how much the pruning actually
cuts down the search space in practice․

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part                           | Estimated Hours |
| ------------------------------ | --------------- |
| Part 1: Problem Analysis       | 0.5             |
| Part 2: Precomputation Design  | 1.5             |
| Part 3: Algorithm Correctness  | 1.0             |
| Part 4: Search Design          | 1.0             |
| Part 5: State and Search Space | 1.5             |
| Part 6: Pruning                | 2.0             |
| Part 7: Implementation         | 2.5             |
| README and DEVLOG writing      | 1.5             |
| **Total**                      | **11.5**        |
