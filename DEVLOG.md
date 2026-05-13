# Development Log – The Torchbearer

**Student Name:** ************\_\_\_************
**Student ID:** ************\_\_\_************

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

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part                           | Estimated Hours |
| ------------------------------ | --------------- |
| Part 1: Problem Analysis       |                 |
| Part 2: Precomputation Design  |                 |
| Part 3: Algorithm Correctness  |                 |
| Part 4: Search Design          |                 |
| Part 5: State and Search Space |                 |
| Part 6: Pruning                |                 |
| Part 7: Implementation         |                 |
| README and DEVLOG writing      |                 |
| **Total**                      |                 |
