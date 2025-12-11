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

1. **Graph Construction:** Edges point from losers to winners, weighted by score difference
2. **Normalization:** Logarithmic scaling smooths extreme values
3. **PageRank:** Iterative algorithm distributes "ranking mass" through the graph
4. **Result:** Teams that beat strong opponents rank higher

**Key Insight:** A win against a highly-ranked team contributes more to your ranking than beating a weak team.

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

#Testing
**1.speed_test.py (Порівняння Швидкості):**
  Цей файл призначений для того, щоб порівняти,
  як швидко працює наш алгоритм PageRank порівняно 
  зі стандартною реалізацією в бібліотеці NetworkX
  Вміст:
  - _readfile(FILENAME)_	Зчитує дані матчів з файлу.
  - _build_graph(data)_	Будує наш граф перемог з вагами (різницею рахунків).
  - _normalize_graph(g)_	Нормалізує ваги графа.
  - _pageRank_weighted(n)_	Запускає наш модифікований PageRank і вимірює "Наш час".
  - _Блок NetworkX_	Будує граф спеціально для NetworkX і запускає
    стандартний nx.pagerank, вимірюючи "NetworkX час"
    
**2.test_logic.py (Перевірка Логіки):**
  Цей файл містить автоматичні тести (pytest),
  які перевіряють, чи всі частини нашого алгоритму працюють правильно.
  Вміст:
  - _test_build_graph_logic_	Перевіряє, що граф будується правильно:
    ребра йдуть від переможця до переможеного, а вага відповідає різниці рахунків.
  - _test_ignore_draws_	Перевіряє, що нічиї (однакові рахунки)
    повністю ігноруються і не створюють зв'язків у графі.
  - _test_normalization_sum_	Перевіряє, що після нормалізації
    сума всіх вихідних ваг з будь-якої команди точно дорівнює 1.0.
  - _test_pagerank_sum_to_one_	Перевіряє, що сума PageRank всіх
    команд у фінальному результаті також точно дорівнює 1.0 (вимога PageRank).

**3.test_benchmark.py (Порівняння Результатів):**
  Цей файл виконує порівняння кінцевих рейтингів,
  отриманих нашим алгоритмом, із результатами, які видає NetworkX.
  Вміст:
  - _test_compare_with_networkx_	Це головний тест. Він обчислює наш рейтинг (team_ranks) та рейтинг NetworkX (nx_ranks) 
  для одного й того ж набору матчів.
  - _Вивід таблиці_	друкує порівняльну таблицю з різницею між двома рейтингами для кожної команди.
  - _assert total_diff < 0.05_	Перевіряє, що загальна різниця між нашим результатом і результатом NetworkX є дуже малою (менше 0.05). Це підтверджує, що наш алгоритм працює правильно і дає надійні результати.
