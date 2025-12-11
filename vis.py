'''
GRAPH VISU TEST
'''

import plotly.graph_objects as go
import networkx as nx

#=========POSSIBLE OUTPUT=========

# номер команди і з ким вона змагалась
test_dict = {1:[1,2, 3, 4, 5, 6, 7, 8], 2:[1,4,8,3,5], 3:[4,5,6,7,8,2,1],\
            4:[3,2], 5:[6], 6:[5,8], 7:[8], 8:[7,6,2]}

# номер команди, назва команди, очки, місце
test_dict_2 = {1: ['ЯСКО 2016', 0, 6],\
            2: ['Лівий Берег', 8, 1],\
            3: ['ФК Гостинний Двір', 0, 5],\
            4:['ДЮСШ 14', 4, 3],\
            5:['Нива', 0, 8],\
            6:['Колос', 1, 4],\
            7: ['Forward', 0, 7],\
            8: ['Вісла', 8, 2]}

match_name = 'SILVER LEAGUE 2015'

#=========FUNCTIONS FOR VISUALISATION=========

def graph_create(data, info):
    '''
    omg
    '''
    graph = nx.DiGraph()

    for circle_id, circle_info in info.items():
        name, score, place = circle_info
        graph.add_node(circle_id, idd=circle_id, name =name,\
            score =score, place=place, size =(((len(data)-place)/(len(data)-1))+1)*30)

    for team, other_list in data.items():
        for other in other_list:
            graph.add_edge(team, other)

    coordinates = nx.spring_layout(graph)
    return (graph, coordinates)

def visu_graph(info,mname):
    '''
    aaa'''
    graph, coordinates = info

    noodle_x =[]
    noodle_y = []
    for noodle in graph.edges():
        x0,y0 = coordinates[noodle[0]]
        x1,y1= coordinates[noodle[1]]
        noodle_x.extend([x0,x1, None])
        noodle_y.extend([y0, y1, None])
    wth = go.Scatter(x=noodle_x, y=noodle_y,
                     line={'width':1.5, 'color':'DarkRed','shape':'spline', 'smoothing':0.2})

    circle_x = []
    circle_y = []
    circle_text = []
    circle_size = []
    circle_team = []

    for circle in graph.nodes():
        x, y = coordinates[circle]
        circle_x.append(x)
        circle_y.append(y)

        name = graph.nodes[circle]['name']
        score = graph.nodes[circle]['score']
        size = graph.nodes[circle]['size']
        place = graph.nodes[circle]['place']

        text = (f'<b>TEAM:</b> {name}<br>'
                f'<b>SCORE:</b> {score}<br>'
                f'<b>PLACE:</b> {place}<br>'
                '<extra></extra>')
        circle_text.append(text)
        circle_size.append(size)
        circle_team.append(str(graph.nodes[circle]['idd']))

    wht = go.Scatter(x=circle_x, y=circle_y,\
                    mode='markers+text', text= circle_team,\
                    textfont={'color': 'White'},hovertemplate=circle_text,
                    marker= dict(opacity=1.0, size=circle_size,\
                                color=circle_size, colorscale='peach',
                                 line_width=2, line_color='DarkRed'))

    visu= go.Figure(data=[wth, wht],
                 layout=go.Layout(title={'text':f'<br>{mname}','font':{'size':25,\
                         'color':'DarkRed'}, 'x':0.5, 'xanchor': 'center'},\
                         showlegend=False, plot_bgcolor="#ffffff",
                hovermode='closest', xaxis=dict(
                    showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    visu.show()


inf = graph_create(test_dict, test_dict_2)
visu_graph(inf, match_name)
