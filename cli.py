import sys
import time
import subprocess
import networkx as nx
from optimized_ranking_table import readfile, build_graph, normalize_graph, pageRank_weighted, writefile
from visualisation import graph_create, edge_create, node_create, visu_graph

def tournament_rank(input_file, output_file=None):
    """Compute PageRank rankings and optionally write to CSV."""
    matches = readfile(input_file)
    graph = build_graph(matches)
    normalized = normalize_graph(graph)
    rankings = pageRank_weighted(normalized)

    if output_file:
        writefile(rankings, output_file)
        print(f"Ranking saved to {output_file}")
    else:
        print("Tournament ranking:")
        sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
        for i, (team, score) in enumerate(sorted_rankings, start=1):
            print(f"{i}. {team}: {score:.6f}")
    return rankings

def tournament_visualisation(input_file):
    """Visualise tournament results using Plotly."""
    matches = readfile(input_file)
    rankings = tournament_rank(input_file)

    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    info_dict = {i+1: [team, score, score*100] for i, (team, score) in enumerate(sorted_rankings)}

    name_to_id = {team: i+1 for i, (team, _) in enumerate(sorted_rankings)}

    game_dict = {i+1: [] for i in range(len(sorted_rankings))}
    for team1, team2, s1, s2 in matches:
        id1 = name_to_id[team1]
        id2 = name_to_id[team2]
        if s1 > s2:
            game_dict[id1].append(id2)
        elif s2 > s1:
            game_dict[id2].append(id1)

    match_name = input_file.replace('.csv', '').upper()
    graph_info = graph_create(game_dict, info_dict)
    edges = edge_create(graph_info)
    nodes = node_create(graph_info)
    visu_graph(edges, nodes, match_name)

def speed_test(input_file):
    """Compare custom PageRank vs NetworkX."""
    print(f"Reading data from {input_file}...")
    start = time.time()
    data = readfile(input_file)
    g = build_graph(data)
    n = normalize_graph(g)
    pageRank_weighted(n)
    print(f"Custom PageRank time: {time.time() - start:.6f} sec")

    nx_graph = nx.DiGraph()
    for t1, t2, s1, s2 in data:
        if s1 > s2:
            nx_graph.add_edge(t2, t1, weight=s1-s2)
        elif s2 > s1:
            nx_graph.add_edge(t1, t2, weight=s2-s1)

    start = time.time()
    nx.pagerank(nx_graph, weight='weight')
    print(f"NetworkX PageRank time: {time.time() - start:.6f} sec")

def run_test(test_file):
    """Run pytest for the given test file."""
    subprocess.run([sys.executable, "-m", "pytest", test_file])

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: tournament <command> [args]")
        print("Commands:")
        print("  rank <input_file> [output_file]")
        print("  visualisation <input_file>")
        print("  speed_test <input_file>")
        print("  test_logic")
        print("  test_benchmark")
        sys.exit(1)

    command = sys.argv[1]

    if command == "rank":
        if len(sys.argv) < 3:
            print("Please provide input file")
            sys.exit(1)
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        tournament_rank(input_file, output_file)

    elif command == "visualisation":
        if len(sys.argv) < 3:
            print("Please provide input file")
            sys.exit(1)
        input_file = sys.argv[2]
        tournament_visualisation(input_file)

    elif command == "speed_test":
        if len(sys.argv) < 3:
            print("Please provide input file")
            sys.exit(1)
        input_file = sys.argv[2]
        speed_test(input_file)

    elif command == "test_logic":
        run_test("test_logic.py")

    elif command == "test_benchmark":
        run_test("test_benchmark.py")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
