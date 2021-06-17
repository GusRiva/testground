import codecs 

with codecs.open('stemma.gv', 'r', 'utf-8') as infile:
    newContent = infile.read()

    newContent += "Resultado"

    with codecs.open('new_stemma.txt', 'w', 'utf-8') as outfile:
        outfile.write(newContent)