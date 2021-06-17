import codecs 
import networkx as nx 
import sys 

changed_file = str(sys.argv[1])

with codecs.open(changed_file, 'r', 'utf-8') as infile:
    newContent = infile.read()

    newContent += "Resultado"

    with codecs.open('./' + changed_file + '.txt', 'w', 'utf-8') as outfile:
        outfile.write(newContent)

G = nx.Graph()

G.add_nodes_from([2, 3])

nx.write_graphml(G,'./' + changed_file + '.graphml',
                 encoding="utf-8")

        