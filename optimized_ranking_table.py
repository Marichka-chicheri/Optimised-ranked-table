"""Галімі квантори"""

import math

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
    graph[node] = {opponent: weight}   (e.g., goal difference)
    """
    nodes = list(graph.keys())
    n = len(nodes)
    node_set = set(nodes)

    # Compute weighted outdegree (sum of weights)
    out_weight = {}
    for node in nodes:
        total = sum(graph[node].get(dest, 0) for dest in graph[node])
        out_weight[node] = total

    # Build reverse graph (incoming weighted edges)
    rev_graph = {node: [] for node in nodes}
    for src, edges in graph.items():
        for dest, w in edges.items():
            if dest in node_set:
                # store: (src, weight)
                rev_graph[dest].append((src, w))

    # initialize ranks
    r = {node: 1.0 / n for node in nodes}

    for _ in range(max_iter):
        new_r = {node: (1 - d) / n for node in nodes}

        # weighted-dangling mass (teams with no outgoing weights)
        dangling_mass = sum(r[node] for node in nodes if out_weight[node] == 0)

        for node in nodes:
            for src, w in rev_graph[node]:
                if out_weight[src] > 0:
                    contribution = r[src] * (w / out_weight[src])
                    new_r[node] += d * contribution
                    # dangling nodes distribute evenly
                    new_r[node] += d * (dangling_mass / n)

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


#Приклад роботи
# graph = build_graph(readfile("matches.csv"))
# normalized_graph = normalize_graph(graph)
# pgrank = pageRank_weighted(normalized_graph)
# writefile(pgrank, "123.csv")
