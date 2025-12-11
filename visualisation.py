'''
GRAPH VISUALISATION
'''

import plotly.graph_objects as go
import networkx as nx
import sys

#========= OUTPUT =========

def readfiles(filename_1, filename_2):
    '''
    Reads files with output
    and returns tuple with 2
    dict and match name.
    '''
    match_name = filename_1.replace('.csv', '').upper()
    info_dict = {}
    name_dict = {}

    with open(filename_2, 'r', encoding='utf-8') as f:
        data = f.readlines()
    for info in data[1:]:
        inf = info.strip().split(',')
        team = int(inf.pop(0))
        name_dict[inf[0]] = team
        info_dict[team] = inf

    with open(filename_1, 'r', encoding='utf-8') as f_2:
        f_2 = f_2.readlines()

    game_dict = {n: [] for n in name_dict.values()}
    for line in f_2[1:]:
        line = line.split(',')[:2]
        team_1 = name_dict[line[0]]
        team_2 = name_dict[line[1]]
        game_dict[team_1].append(team_2)
        game_dict[team_2].append(team_1)

    return (match_name, game_dict, info_dict)


#=========FUNCTIONS FOR VISUALISATION=========

def graph_create(data, info):
    '''
    Creates graph.
    '''
    graph = nx.DiGraph()

    for circle_id, circle_info in info.items():
        name, score, place = circle_info
        graph.add_node(circle_id, idd=circle_id, name =name,\
            score =score, place=place, size =(((len(data)-circle_id)/(len(data)-1))+1)*30)

    for team, other_list in data.items():
        for other in other_list:
            graph.add_edge(team, other)

    coordinates = nx.spring_layout(graph)
    return (graph, coordinates)

def edge_create(info):
    '''
    creates edge'''
    graph, coordinates = info

    noodle_x =[]
    noodle_y = []
    for noodle in graph.edges():
        x0,y0 = coordinates[noodle[0]]
        x1,y1= coordinates[noodle[1]]
        noodle_x.extend([x0,x1, None])
        noodle_y.extend([y0, y1, None])
    edges = go.Scatter(x=noodle_x, y=noodle_y,
                     line={'width':1.5, 'color':'DarkRed','shape':'spline', 'smoothing':0.2})
    return edges

def node_create(info):
    '''
    Creates nodes
    '''
    graph, coordinates = info


    circle_x = []
    circle_y = []
    circle_text = []
    circle_size = []
    circle_team = []

    for circle in graph.nodes():
        circle_x.append(coordinates[circle][0])
        circle_y.append(coordinates[circle][1])

        name = graph.nodes[circle]['name']
        score = graph.nodes[circle]['score']
        place = graph.nodes[circle]['place']

        text = (f'<b>TEAM:</b> {name}<br>'
                f'<b>SCORE:</b> {score}<br>'
                f'<b>PERCENTAGE:</b> {place}%<br>'
                '<extra></extra>')
        circle_text.append(text)
        circle_size.append(graph.nodes[circle]['size'])
        # circle_team.append(str(graph.nodes[circle]['idd']))
        if graph.nodes[circle]['idd'] == 1:
            circle_team.append(str(graph.nodes[circle]['idd'])+'<br>🥇')
        elif graph.nodes[circle]['idd'] == 2:
            circle_team.append(str(graph.nodes[circle]['idd'])+'<br>🥈')
        elif graph.nodes[circle]['idd'] == 3:
            circle_team.append(str(graph.nodes[circle]['idd'])+'<br>🥉')
        else:
            circle_team.append(str(graph.nodes[circle]['idd']))

    nodes = go.Scatter(x=circle_x, y=circle_y,\
                    mode='markers+text', text= circle_team,\
                    textfont={'color': 'White'},hovertemplate=circle_text,
                    marker= {'opacity':1.0, 'size':circle_size,\
                                'color':circle_size, 'colorscale':'peach',
                                 'line_width':2, 'line_color':'DarkRed'})
    return nodes

def visu_graph(edges, nodes,mname):
    '''
    Graph visualisation in web
    wih plotly.
    '''
    visu= go.Figure(data=[edges, nodes],
                 layout=go.Layout(title={'text':f'<br>{mname}','font':{'size':25,\
                         'color':'DarkRed'}, 'x':0.5, 'xanchor': 'center'},\
                         showlegend=False, plot_bgcolor="#ffffff",
                hovermode='closest', xaxis={
                    'showgrid':False, 'zeroline':False, 'showticklabels':False},
                yaxis={'showgrid':False, 'zeroline':False, 'showticklabels':False}))

    visu.show()


#========= TEST =========

# m_name, dict_1, dict_2 = readfiles('test2.csv','test.csv')
# g = graph_create(dict_1, dict_2)
# print(m_name, dict_1, dict_2)
# visu_graph(edge_create(g), node_create(g), m_name)
