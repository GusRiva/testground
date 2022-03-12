import os 
import glob 

try:
    print('Testing folder structure...')
    # valid_folder_structure = set("data", "CITATION.cff", "examples", "example_graph.png", "LICENSE", "README.md",
    #             "schema", "tests", "transform")
    # actual_folder_structure = os.listdir('.')
except:
    print('Root folder structure should not be modified (submissions go in database/LANG/EDITOR_TITLE_DATE')
else:
    print('Folder Structure Correct')



for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
    print("Checking", file)