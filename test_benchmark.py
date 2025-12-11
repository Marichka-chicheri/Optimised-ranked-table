import networkx as nx
import pytest
from optimized_ranking_table import build_graph, normalize_graph, pageRank_weighted

def test_compare_with_networkx():
    """
    Порівнює нашу реалізацію PageRank з еталонною реалізацією NetworkX.
    Примітка: Оскільки NetworkX має трохи іншу логіку обробки висячих нікців,
    ми перевіряємо кореляцію або близькість значень, а не ідеальну точність до 1e-8.
    """
    matches = [
        ("TeamA", "TeamB", 3, 0),
        ("TeamB", "TeamC", 2, 1),
        ("TeamC", "TeamA", 1, 0),
        ("TeamD", "TeamA", 0, 5),
    ]

    team_graph_raw = build_graph(matches)
    team_graph_norm = normalize_graph(team_graph_raw)
    team_ranks = pageRank_weighted(team_graph_norm, d=0.85, max_iter=1000)

    nx_graph = nx.DiGraph()
    for source, targets in team_graph_norm.items():
        for target, weight in targets.items():
            nx_graph.add_edge(source, target, weight=weight)

    for team in team_ranks.keys():
        if not nx_graph.has_node(team):
            nx_graph.add_node(team)

    nx_ranks = nx.pagerank(nx_graph, alpha=0.85, weight='weight', tol=1e-8, max_iter= 10000)

    print("\n--- Порівняймо ---")
    print(f"{'Team':<10} | {'Team Rank':<10} | {'NX Rank':<10} | {'Difference':<10}")
    
    total_diff = 0
    for team in team_ranks:
        r_dev = team_ranks[team]
        r_nx = nx_ranks.get(team, 0)
        diff = abs(r_dev - r_nx)
        total_diff += diff
        print(f"{team:<10} | {r_dev:.6f}   | {r_nx:.6f}   | {diff:.6f}")
    assert total_diff < 0.05, "Відхилення від NetworkX too much!"

if __name__ == "__main__":
    test_compare_with_networkx()
