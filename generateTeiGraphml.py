import codecs 
import networkx as nx 
import sys 
import re 
from lxml import etree as et 

if len(sys.argv) > 1:
    changed_file = str(sys.argv[1])
else:
    changed_file = "/home/gustavo/Dokumente/OpenStemmata/test/Isopet.gv"

with codecs.open(changed_file, 'r', 'utf-8') as dotfile:
    lines = dotfile.readlines()
    nodes = {}
    edges = []
    for line in lines:
        noAttrib = re.sub('\'.+?\'', '', line) 
        noAttrib = re.sub('".+?"', '', line)
        if "->" in noAttrib or "--" in noAttrib:
            origin = re.split('->', noAttrib)[0].strip()
            dest = re.split('->', noAttrib)[1].strip()
            if '[' in dest:
                dest = re.split('\[', dest)[0].strip()
            if ';' in dest:
                dest = re.split(';', dest)[0].strip()
            if origin not in nodes:
                nodes[origin] = {}
            if dest not in nodes:
                nodes[dest] = {}
            edge_attr = {}
            if '[' in noAttrib:
                attributes = re.findall('(\w+)="(\w*)",?\s?', line)    
                for attr in attributes:
                    if attr[0] == 'style' and attr[1] == 'dashed':
                        edge_attr['type'] = 'contamination'
            edges.append((origin,dest, edge_attr))
            
        elif '[' in noAttrib:
            node = re.split('\[', noAttrib)[0].strip()
            nodes[node] = {}
            attributes = re.findall('(\w+)="(\w*)",?\s?', line)
            for attr in attributes:
                nodes[node][attr[0]] = attr[1]

nodes = [ (x,nodes[x]) for x in nodes ]

G = nx.Graph()
# print(edges)
G.add_nodes_from(nodes)
G.add_edges_from(edges)

nx.write_graphml(G, changed_file[0:-3] + '.graphml', encoding="utf-8")

graph = et.Element('graph')
tree = et.ElementTree(graph)
graph.attrib['type'] = 'directed'

for node in G.nodes(data=True):
    # print(node)
    nodeEl = et.SubElement(graph, 'node', attrib={'{http://www.w3.org/XML/1998/namespace}id': "n_" + node[0]})
    labelEl = et.SubElement(nodeEl, 'label')
    if 'label' in node[1]:
        label = node[1]['label']
        if not re.match(r'^\s*$', label):   
            labelEl.text = label   
        else:
            labelEl.text = ''  
    else:
        labelEl.text = node[0]  
    if 'color' in node[1]:
        color = node[1]['color']
        if color == 'grey':
            nodeEl.attrib['type'] = 'hypothetical'
        else:
            nodeEl.attrib['type'] = 'witness'
    else:
        nodeEl.attrib['type'] = 'witness'
            
for edge in G.edges(data=True):
    et.SubElement(graph, 'arc', attrib= {'from': "#n_" + edge[0], 'to': "#n_" + edge[1]})


tree.write( changed_file[0:-3] + '.tei.xml', pretty_print=True, encoding="UTF-8", xml_declaration=True)




        