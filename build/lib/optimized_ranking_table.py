"""Галімі квантори"""

import math
import sys

def readfile(filename):
    """
    Docstring for readfile

    :param filename: Description
    """
    with open(filename, 'r', encoding='utf-8') as file:
        matches = []
        lines = file.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            parts = line.strip().split(',')

            team1 = parts[0]
            team2 = parts[1]
            score_team1 = int(parts[2])
            score_team2 = int(parts[3])
            matches.append((team1, team2, score_team1, score_team2))
    return matches

def build_graph(matches):
    """
    Docstring for build_graph

    :param matches: Description
    """
    graph_of_winners = {}
    for match in matches:
        team1, team2, score_team1, score_team2 = match

        if team1 not in graph_of_winners:
            graph_of_winners[team1] = {}
        if team2 not in graph_of_winners:
            graph_of_winners[team2] = {}

        if score_team1 > score_team2:
            diff = score_team1 - score_team2
            if team1 not in graph_of_winners[team2]:
                graph_of_winners[team2][team1] = 0
            graph_of_winners[team2][team1] += diff
        elif score_team2 > score_team1:
            diff = score_team2 - score_team1
            if team2 not in graph_of_winners[team1]:
                graph_of_winners[team1][team2] = 0
            graph_of_winners[team1][team2] += diff
        else:
            continue
    return graph_of_winners

def normalize_graph(graph: dict):
    """
    Docstring for normalize_graph

    :param graph: Description
    :type graph: dict
    """
    normalized_graph = {}
    for team, opponents in graph.items():
        log_weight = {}
        if not opponents:
            normalized_graph[team] = {}
            continue

        for opp, count in opponents.items():
            log_weight[opp] = 1 + math.log(count + 1)
        total = sum(log_weight.values())
        normalized_graph[team] = {}
        for opp, count in log_weight.items():
            normalized_graph[team][opp] = count/total

    return normalized_graph



def pageRank_weighted(graph, d=0.85, tol=1e-8, max_iter=200):
    """
    Compute the weighted PageRank of a directed graph with correct handling
    of dangling nodes (nodes with no outgoing edges).

    Parameters
    ----------
    graph : dict
        A dictionary representing the weighted directed graph in adjacency form:
        {
            node_u: {node_v: weight_uv, ...},
            ...
        }
        Edges are assumed to be outgoing from `node_u` toward `node_v`.
        All edge weights must be non-negative.

    d : float, optional (default=0.85)
        Damping factor (probability of continuing the random walk). Must be in (0, 1).

    tol : float, optional (default=1e-8)
        Convergence tolerance. The iteration stops when the L1 norm of the
        change in PageRank scores is below this threshold.

    max_iter : int, optional (default=200)
        Maximum number of power iterations to perform.

    Returns
    -------
    dict
        A dictionary mapping each node to its normalized PageRank score.
        The scores sum to 1.

    Notes
    -----
    - Dangling nodes (nodes with zero weighted outdegree) contribute their
      entire PageRank mass uniformly to all nodes at every iteration.
    - This implementation performs the standard PageRank power iteration:

        PR_new(v) =
            (1 - d)/N
          + d * (dangling_mass / N)
          + d * sum_{u->v} PR(u) * (weight_uv / out_weight(u))

    - The algorithm is guaranteed to converge for 0 < d < 1.
    """
    nodes = list(graph.keys())
    n = len(nodes)
    node_set = set(nodes)

    # Compute weighted outdegree (sum of weights)
    out_weight = {node: sum(graph[node].values()) for node in nodes}

    # Build reverse graph (incoming weighted edges)
    rev_graph = {node: [] for node in nodes}
    for src, edges in graph.items():
        for dest, w in edges.items():
            if dest in node_set:
                rev_graph[dest].append((src, w))

    # initialize ranks
    r = {node: 1.0 / n for node in nodes}

    for _ in range(max_iter):
        dangling_mass = sum(r[node] for node in nodes if out_weight[node] == 0)

        dangling_contribution = d * (dangling_mass / n)
        new_r = {node: (1.0 - d) / n + dangling_contribution for node in nodes}

        for dest_node in nodes:
            for src, w in rev_graph[dest_node]:
                if out_weight[src] > 0:
                    contribution = r[src] * (w / out_weight[src])
                    new_r[dest_node] += d * contribution

        # check convergence
        diff = sum(abs(new_r[n] - r[n]) for n in nodes)
        if diff < tol:
            break

        r = new_r

    # normalize
    total = sum(r.values())
    return {team: rank / total for team, rank in r.items()}



def writefile(rankings: dict, filepath):
    """
    Docstring for writefile

    :param rankings: Description
    :type rankings: dict
    :param filepath: Description
    """
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write("#rank,team,pagerank,percantage\n")
        for rank, (team, score) in enumerate(sorted_rankings, start=1):
            percentage = score * 100
            file.write(f"{rank},{team},{score:.6f},{percentage:.2f}\n")

# def main():
#     """Main entry point for CLI"""
#     if len(sys.argv) > 1:
#         if sys.argv[1] == 'file' and len(sys.argv) > 2:
#             readfile(sys.argv[2])
#         else:
#             print("Usage:")
#             print("  tournament example")
#             print("  tournament file <filename>")
def main():
    """CLI entry point for ranking tournament teams."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  tournament rank <input_file> [output_file]")
        print()
        print("Приклади:")
        print("  tournament rank matches.csv")
        print("  tournament rank matches.csv ranking.csv")
        sys.exit(1)

    command = sys.argv[1]

    if command != "rank":
        print(f"Unknown command: {command}")
        print("Use: tournament rank <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    # 1. Read matches
    try:
        matches = readfile(input_file)
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    # 2. Build graph
    graph = build_graph(matches)

    # 3. Normalize
    normalized = normalize_graph(graph)

    # 4. PageRank
    rankings = pageRank_weighted(normalized)

    # 5. Output
    if output_file:
        writefile(rankings, output_file)
        print(f"Ranking saved to {output_file}")
    else:
        print("Tournament ranking:")
        sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
        for i, (team, score) in enumerate(sorted_rankings, start=1):
            print(f"{i}. {team}: {score:.6f}")

if __name__ == "__main__":
    main()

#Приклад роботи
# graph = build_graph(readfile("matches.csv"))
# normalized_graph = normalize_graph(graph)
# pgrank = pageRank_weighted(normalized_graph)
# writefile(pgrank, "123.csv")
