import codecs 
import networkx as nx 

with codecs.open('./stemma.gv', 'r', 'utf-8') as infile:
    newContent = infile.read()

    newContent += "Resultado"

    with codecs.open('./new_stemma.txt', 'w', 'utf-8') as outfile:
        outfile.write(newContent)

G = nx.Graph()

G.add_nodes_from([2, 3])

nx.write_graphml(G,'./new_stemma.graphml',
                 encoding="utf-8")

        