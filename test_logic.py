import pytest
from optimized_ranking_table import build_graph, normalize_graph, pageRank_weighted

"""
This file perfectly tests logic
of optimized_ranking_table.py



To make a testing print
<pytest test_logic.py> 
in terminal in the same
directory as files
"""

def simple_matches():
    return [
        ("D", "S", 3, 1),
        ("S", "Z", 2, 0),
        ("Z", "D", 1, 0),
        ("B", "A", 10, 0),
    ]
matches = simple_matches()

def test_build_graph_logic(matches:list):
    graph = build_graph(matches)
    assert 'S' in graph
    assert 'D' in graph['S']
    if "D" in graph:
        assert 'S' not in graph['D']
    assert graph['S']['D'] == 2

def test_ignore_draws():
    test_match = [('A', 'B', 2, 2)]
    graph = build_graph(test_match)
    if 'A' in graph:
        assert graph['A'] == {}
    if 'B' in graph:
        assert graph['B'] == {}

def test_normalization_sum(matches):
    graph = build_graph(matches)
    norm_graph = normalize_graph(graph)
    weights = norm_graph["S"].values()
    weights_two = norm_graph["Z"].values()
    # pytest.approx потрібен, щоби округлити
    assert sum(weights) == pytest.approx(1.0)
    assert sum(weights_two) == pytest.approx(1.0)

def test_pagerank_sum_to_one(matches):
    graph = build_graph(matches)
    norm_graph = normalize_graph(graph)
    ranks = pageRank_weighted(norm_graph)
    result = ranks.values()
    # Сума PageRank завжди мала б бути 1
    assert sum(result) == pytest.approx(1.0)

def test_gian_score(matches):
    graph = build_graph(matches)
    assert 'A' in graph
    assert 'B' in graph['A']
    if "B" in graph:
        assert 'A' not in graph['B']
    assert graph['A']['B'] == 10
