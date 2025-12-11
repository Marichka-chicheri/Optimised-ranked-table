# Optimised-ranked-table
v2∙LatestCopyPublishTournament Ranking System
A tournament ranking system based on the PageRank algorithm that analyzes match results to compute team rankings.
Overview
This project implements a sports team ranking system using a modified PageRank algorithm. The system processes match results and generates rankings based on wins and score differences.
Core Functions
readfile(filename)
Reads match results from a CSV file.
Parameters:

filename (str): Path to the input CSV file

Returns:

list: List of tuples containing (team1, team2, score_team1, score_team2)

Behavior:

Skips lines starting with # (comments)
Parses each line as: team1,team2,score1,score2
Converts scores to integers


build_graph(matches)
Constructs a directed graph representing the tournament results.
Parameters:

matches (list): List of match tuples from readfile()

Returns:

dict: Graph structure where {loser: {winner: score_difference}}

Behavior:

Creates edges from losing teams to winning teams
Edge weight equals the score difference
Ignores draws (matches with equal scores)
Accumulates weights if teams play multiple times

Example:
python# If TeamA beats TeamB 3-1 and 2-0
# Graph: {TeamB: {TeamA: 5}}  # 5 = (3-1) + (2-0)

normalize_graph(graph)
Normalizes graph edge weights using logarithmic scaling.
Parameters:

graph (dict): Raw graph from build_graph()

Returns:

dict: Normalized graph with weights between 0 and 1

Behavior:

Applies transformation: weight = 1 + log(count + 1)
Normalizes weights so outgoing edges from each node sum to 1
Handles teams with no wins (empty outgoing edges)

Purpose:
Logarithmic scaling prevents teams with large score differences from dominating the ranking unfairly.

pageRank_weighted(graph, d=0.85, tol=1e-8, max_iter=200)
Computes weighted PageRank scores for all teams.
Parameters:

graph (dict): Normalized weighted directed graph
d (float): Damping factor, default 0.85
tol (float): Convergence tolerance, default 1e-8
max_iter (int): Maximum iterations, default 200

Returns:

dict: Dictionary mapping each team to its PageRank score (sum = 1)

Algorithm:
PR(v) = (1-d)/N + d*(dangling_mass/N) + d*Σ(PR(u) * w(u,v) / out_weight(u))
Where:

PR(v) - PageRank of team v
N - Total number of teams
w(u,v) - Normalized edge weight from u to v
out_weight(u) - Sum of all outgoing weights from u
dangling_mass - Total PageRank of teams with no wins

Convergence:
Iterates until the L1 norm of rank changes is below tol or max_iter is reached.

writefile(rankings, filepath)
Writes rankings to a CSV file.
Parameters:

rankings (dict): Team rankings from pageRank_weighted()
filepath (str): Output file path

Output Format:
csv#rank,team,pagerank,percentage
1,TeamA,0.350000,35.00
2,TeamB,0.280000,28.00
Behavior:

Sorts teams by PageRank in descending order
Assigns ranks starting from 1
Converts PageRank to percentage (×100)


main()
CLI entry point for the ranking system.
Usage:
bashpython tournament.py rank <input_file> [output_file]
Workflow:

Validates command-line arguments
Reads matches using readfile()
Builds graph using build_graph()
Normalizes graph using normalize_graph()
Computes rankings using pageRank_weighted()
Outputs results (file or console)

Examples:
bash# Print rankings to console
python tournament.py rank matches.csv

# Save rankings to file
python tournament.py rank matches.csv rankings.csv

Input File Format
CSV format with match results:
csv# Comments start with #
TeamA,TeamB,3,1
TeamB,TeamC,2,2
TeamC,TeamA,1,0
Each line: team1,team2,score1,score2

How It Works

Graph Construction: Edges point from losers to winners, weighted by score difference
Normalization: Logarithmic scaling smooths extreme values
PageRank: Iterative algorithm distributes "ranking mass" through the graph
Result: Teams that beat strong opponents rank higher

Key Insight: A win against a highly-ranked team contributes more to your ranking than beating a weak team










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
