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
- Accumulates weights if teams play multiple times

---

### 3. normalize_graph(graph)

Normalizes graph edge weights using logarithmic scaling.

**Parameters:** 
- `graph` (dict) - Raw graph from `build_graph()`

**Returns:** 
- Normalized graph with weights between 0 and 1

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

## CLI
### cli.py
The file provides a command-line interface for analysing tournament results using a custom weighted PageRank algorithm. It allows us to:
- Compute team rankings from a CSV file and optionally save them to another file.
- Visualise tournament outcomes using interactive Plotly-based graphs.
- Benchmark performance by comparing the custom PageRank implementation to NetworkX’s built-in PageRank.

### setup.py
The file configures the Python package optimized-ranking-table. It defines the package metadata (name, version, authors, description) and specifies which Python modules are included in the distribution. It also registers a console command: *tournament*, which runs the CLI defined in cli.py.

### How does CLI work?
- Firstly you need to open terminal in Python or CMD.
- Write pip install . to install all requirement libraries.
- Then write "tournament" to see the list of commands.
  **Commands:**
  - tournament rank <input_file> - shows you the ranking table with the results in terminal.
  - tournament rank <input_file> [output_file] - writes down the ranking table into a file.
  - tournament visualisation <input_file> - opens a page with the visualised garph.
  - tournament speed_test <input_file> - shows how quick our own PageRank implementation is compared to the built-in PageRank algorithm from the NetworkX library.
  - tournament test_logic = shows how good our code works, if there are some problems.
  - tournament test_benchmark - shows whether our own implementation of the PageRank algorithm (pageRank_weighted) performs approximately the same as the    reference implementation in the NetworkX library.


