# Optimised-ranking-table

## Tournament Ranking System

A tournament ranking system based on the PageRank algorithm that analyzes match results to compute team rankings.

## Core Functions

### 1. readfile(filename)

Reads match results from a CSV file.

**Parameters:** 
- `filename` (str) - Path to the input CSV file

**Returns:** 
- List of tuples containing `(team1, team2, score_team1, score_team2)`

**Behavior:** 
- Skips lines starting with `#` (comments)
- Parses each line as: `team1,team2,score1,score2`
- Converts scores to integers

---

### 2. build_graph(matches)

Constructs a directed graph representing the tournament results.

**Parameters:** 
- `matches` (list) - List of match tuples from `readfile()`

**Returns:** 
- Dictionary where `{loser: {winner: score_difference}}`

**Behavior:**
- Creates edges from losing teams to winning teams
- Edge weight equals the score difference
- Ignores draws (matches with equal scores)
- Accumulates weights if teams play multiple times

---

### 3. normalize_graph(graph)

Normalizes graph edge weights using logarithmic scaling.

**Parameters:** 
- `graph` (dict) - Raw graph from `build_graph()`

**Returns:** 
- Normalized graph with weights between 0 and 1

**Behavior:**
- Applies transformation: `weight = 1 + log(count + 1)`
- Normalizes weights so outgoing edges from each node sum to 1
- Handles teams with no wins (empty outgoing edges)

**Purpose:** 
- Logarithmic scaling prevents teams with large score differences from dominating the ranking unfairly

---

### 4. pageRank_weighted(graph, d=0.85, tol=1e-8, max_iter=200)

Computes weighted PageRank scores for all teams.

**Parameters:** 
- `graph` (dict) - Normalized weighted directed graph
- `d` (float) - Damping factor, default 0.85
- `tol` (float) - Convergence tolerance, default 1e-8
- `max_iter` (int) - Maximum iterations, default 200

**Returns:** 
- Dictionary mapping each team to its PageRank score (sum = 1)

**Algorithm:** 

```
PR(v) = (1-d)/N + d*(dangling_mass/N) + d*Σ(PR(u) * w(u,v) / out_weight(u))
```

**Convergence:** 
- Iterates until the L1 norm of rank changes is below `tol` or `max_iter` is reached

---

### 5. writefile(rankings, filepath)

Writes rankings to a CSV file.

**Parameters:** 
- `rankings` (dict) - Team rankings from `pageRank_weighted()`
- `filepath` (str) - Output file path

**Output Format:**

```csv
#rank,team,pagerank,percentage
1,TeamA,0.350000,35.00
2,TeamB,0.280000,28.00
```

**Behavior:**
- Sorts teams by PageRank in descending order
- Assigns ranks starting from 1
- Converts PageRank to percentage (×100)

---

### 6. main()

CLI entry point for the ranking system.

**Usage:** 

```bash
python tournament.py rank <input_file> [output_file]
```

**Workflow:**
1. Validates command-line arguments
2. Reads matches using `readfile()`
3. Builds graph using `build_graph()`
4. Normalizes graph using `normalize_graph()`
5. Computes rankings using `pageRank_weighted()`
6. Outputs results (file or console)

---

## Input File Format

CSV format with match results:

```csv
# Comments start with #
TeamA,TeamB,3,1
TeamB,TeamC,2,2
TeamC,TeamA,1,0
```

Each line: `team1,team2,score1,score2`

---

## How It Works

### Overview

The system uses a four-step process to rank tournament teams:

1. **Graph Construction:** Edges point from losers to winners, weighted by score difference
2. **Normalization:** Logarithmic scaling smooths extreme values
3. **PageRank:** Iterative algorithm distributes "ranking mass" through the graph
4. **Result:** Teams that beat strong opponents rank higher

**Key Insight:** A win against a highly-ranked team contributes more to your ranking than beating a weak team.

---

### PageRank Algorithm Explained

PageRank is an algorithm originally developed by Google founders to rank web pages. In our tournament context, we adapt it to rank sports teams based on match results.

#### The Core Concept

Think of PageRank as a "voting system" where:
- Each team has a certain amount of "ranking power"
- When Team A beats Team B, Team B essentially "votes" for Team A
- The strength of this vote depends on how much ranking power Team B has
- Teams gain ranking power by beating other strong teams

#### The Mathematical Formula

```
PR(v) = (1-d)/N + d*(dangling_mass/N) + d*Σ(PR(u) * w(u,v) / out_weight(u))
```

**Breaking it down:**
- `PR(v)` - The PageRank score for team v (what we're calculating)
- `(1-d)/N` - Base probability (every team gets a minimum score)
- `d` - Damping factor (0.85) - represents the probability of "following" a connection
- `N` - Total number of teams in the tournament
- `dangling_mass` - Total ranking power from teams with no wins (redistributed equally)
- `Σ(PR(u) * w(u,v) / out_weight(u))` - Sum of weighted votes from teams that lost to v

#### How the Iteration Works

1. **Initialization:** Every team starts with equal ranking: `PR = 1/N`
2. **Iteration:** In each step, we recalculate each team's ranking based on:
   - Who they beat (incoming edges)
   - How strong those beaten teams are (their current PageRank)
   - The score difference (edge weight)
3. **Convergence:** We repeat until rankings stabilize (change less than 0.00000001)
4. **Normalization:** Final scores sum to 1.0 (100%)

#### Example Scenario

Consider three teams:
- Team A beats Team B (3-1)
- Team B beats Team C (2-0)  
- Team A beats Team C (5-1)

**Initial ranks:** A=0.333, B=0.333, C=0.333

**After iteration:**
- Team A gains ranking power from both B and C
- Team B gains some power from C
- Team C has no wins, so loses ranking power

**Final ranks (example):** A=0.50, B=0.35, C=0.15

#### What PageRank Returns

The `pageRank_weighted()` function returns a dictionary:

```python
{
    'TeamA': 0.285430,  # 28.54% of total ranking power
    'TeamB': 0.245821,  # 24.58%
    'TeamC': 0.223147,  # 22.31%
    'TeamD': 0.245602   # 24.56%
}
```

**Interpretation:**
- Values are between 0 and 1
- Sum of all values equals exactly 1.0
- Higher value = stronger team
- Can be converted to percentage (multiply by 100)
- Can be used to create ordered rankings (1st, 2nd, 3rd, etc.)

#### Why PageRank Works Well for Tournaments

1. **Transitive strength:** If A beats B and B beats C, A gets credit for indirectly dominating C
2. **Quality wins matter:** Beating the #1 team boosts your rank more than beating the #10 team
3. **Score differences count:** Winning 5-0 matters more than winning 1-0
4. **Handles cycles:** Works even when A beats B, B beats C, and C beats A
5. **No single metric:** Uses the entire graph structure, not just win/loss records

---

## Testing

### 1. speed_test.py (Performance Comparison)

This file compares how fast our PageRank algorithm works compared to the standard implementation in the NetworkX library.

**Contents:**
- `readfile(FILENAME)` - Reads match data from file
- `build_graph(data)` - Builds our victory graph with weights (score differences)
- `normalize_graph(g)` - Normalizes graph weights
- `pageRank_weighted(n)` - Runs our modified PageRank and measures "Our time"
- **NetworkX Block** - Builds a graph specifically for NetworkX and runs standard `nx.pagerank`, measuring "NetworkX time"

---

### 2. test_logic.py (Logic Verification)

This file contains automatic tests (pytest) that verify all parts of our algorithm work correctly.

**Contents:**
- `test_build_graph_logic` - Verifies that the graph is built correctly: edges go from winner to loser, and weight corresponds to score difference
- `test_ignore_draws` - Verifies that draws (equal scores) are completely ignored and don't create links in the graph
- `test_normalization_sum` - Verifies that after normalization, the sum of all outgoing weights from any team equals exactly 1.0
- `test_pagerank_sum_to_one` - Verifies that the sum of PageRank for all teams in the final result also equals exactly 1.0 (PageRank requirement)

---

### 3. test_benchmark.py (Results Comparison)

This file performs a comparison of final rankings obtained by our algorithm with results produced by NetworkX.

**Contents:**
- `test_compare_with_networkx` - This is the main test. It calculates our ranking (team_ranks) and NetworkX ranking (nx_ranks) for the same set of matches
- **Table Output** - Prints a comparison table with the difference between the two rankings for each team
- `assert total_diff < 0.05` - Verifies that the total difference between our result and NetworkX result is very small (less than 0.05). This confirms that our algorithm works correctly and produces reliable results

---

## Project Structure

```
tournament-ranking/
├── optimized_ranking_table.py   # Core ranking algorithm
├── visualisation.py             # Graph visualization
├── speed_test.py                # Performance comparison
├── test_logic.py                # Logic unit tests
├── test_benchmark.py            # Benchmark tests
├── setup.py                     # SLI
├── matches.csv                  # Example input data
├── matches_uni.csv              # Additional data file for checks
├── test_matches.csv             # Data for testing
└── README.md                    # Project documentation
```


