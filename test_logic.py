""" testing """
import pytest
from optimized_ranking_table import build_graph, normalize_graph, pageRank_weighted

matches = [("D", "S", 3, 1),("S", "Z", 2, 0),("Z", "D", 1, 0),("B", "A", 10, 0),]

def test_build_graph_logic(match: list):
    """
    Tests the basic logic of the build_graph function using a sample match.

    It verifies:
    1. The 'S' node (winning team/entity) is present in the graph.
    2. An edge exists from 'S' to 'D' (loser) in the graph structure.
    3. The graph is directed: there is NO reverse edge from 'D' to 'S'.
    4. The weight of the edge from 'S' to 'D' is correctly set to 2.
    """
    graph = build_graph(match)
    assert 'S' in graph
    assert 'D' in graph['S']
    if "D" in graph:
        assert 'S' not in graph['D']
    assert graph['S']['D'] == 2


def test_normalization_sum(match):
    """
    Tests the normalization logic to ensure outgoing edge weights sum to 1.0.

    It verifies that for two sample nodes ('S' and 'Z') in the normalized graph:
    1. The sum of all outgoing weights from 'S' is approximately 1.0.
    2. The sum of all outgoing weights from 'Z' is approximately 1.0.

    Uses pytest.approx for floating-point comparison, which is necessary for
    checking sums that should equal 1.0 after division/normalization.
    """
    graph = build_graph(match)
    norm_graph = normalize_graph(graph)
    weights = norm_graph["S"].values()
    weights_two = norm_graph["Z"].values()
    # pytest.approx is needed to handle rounding
    assert sum(weights) == pytest.approx(1.0)
    assert sum(weights_two) == pytest.approx(1.0)

def test_pagerank_sum_to_one(match):
    """
    Tests the fundamental property of the PageRank algorithm.

    It verifies that the sum of all PageRank scores for all nodes in the graph
    must be approximately 1.0 (or 100%).

    The PageRank calculation is performed on the normalized graph.
    """
    graph = build_graph(match)
    norm_graph = normalize_graph(graph)
    ranks = pageRank_weighted(norm_graph)
    result = ranks.values()
    # The sum of PageRank should always be 1
    assert sum(result) == pytest.approx(1.0)

def test_gian_score(match):
    """
    Tests a specific case of graph building where the weight/score is high (e.g., 10).

    It verifies:
    1. The winning team 'A' is present.
    2. An edge exists from the winner 'A' to the loser 'B'.
    3. The graph is directed: there is NO reverse edge from 'B' to 'A'.
    4. The edge weight (score difference or count) from 'A' to 'B' is correctly set to 10.
    """
    graph = build_graph(match)
    assert 'A' in graph
    assert 'B' in graph['A']
    if "B" in graph:
        assert 'A' not in graph['B']
    assert graph['A']['B'] == 10
