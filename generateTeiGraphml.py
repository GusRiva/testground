import codecs 
import networkx as nx 
import sys 
import re 
from lxml import etree as et 

changed_file = str(sys.argv[1])

# with codecs.open(changed_file, 'r', 'utf-8') as infile:
#     newContent = infile.read()

#     newContent += "Resultado"

#     with codecs.open('./' + changed_file + '.txt', 'w', 'utf-8') as outfile:
#         outfile.write(newContent)

# G = nx.Graph()

# G.add_nodes_from([2, 3])

# # Modify the file extension
# nx.write_graphml(G,'./' + changed_file + '.graphml',
#                  encoding="utf-8")




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
            edges.append((origin,dest))
        elif '[' in noAttrib:
            node = re.split('\[', noAttrib)[0].strip()
            nodes[node] = {}
            attributes = re.findall('(\w+)="(\w*)",?\s?', line)
            for attr in attributes:
                nodes[node][attr[0]] = attr[1]
            
graphEl = et.Element('graph')
graph = et.ElementTree(graphEl)
graphEl.attrib['type'] = 'directed'
for node in nodes:
    nodeEl = et.SubElement(graphEl, 'node', attrib={'{http://www.w3.org/XML/1998/namespace}id': node})
    labelEl = et.SubElement(nodeEl, 'label')
    if 'label' in nodes[node]:
        label = nodes[node]['label']
        if not re.match(r'^\s*$', label):   
            labelEl.text = label   
    if 'color' in nodes[node]:
        color = nodes[node]['color']
        if color == 'grey':
            nodeEl.attrib['type'] = 'hypothetical'
        else:
            nodeEl.attrib['type'] = 'witness'
            






        