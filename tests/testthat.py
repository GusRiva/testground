import os 
import glob 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    print('Testing folder structure...')
    # valid_folder_structure = set("data", "CITATION.cff", "examples", "example_graph.png", "LICENSE", "README.md",
    #             "schema", "tests", "transform")
    actual_folder_structure = os.listdir('.')
    print(actual_folder_structure)
except:
    print('Root folder structure should not be modified (submissions go in database/LANG/EDITOR_TITLE_DATE')
else:
    print(f"{bcolors.OKGREEN}Folder Structure Correct{bcolors.ENDC}")



for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
    print("Checking", file)