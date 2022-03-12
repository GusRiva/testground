import os 
import glob 
import unittest
import sys

exit_code = 0

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

# try:
print('Testing folder structure...')
valid_folder_structure =  [".git", ".gitignore", ".github", "data", "CITATION.cff", "examples", "example_graph.png", "LICENSE", "README.md",
            "schema", "tests", "transform"]
actual_folder_structure = os.listdir('.')
try:
    for el in actual_folder_structure:
        # unittest.assertIn(el, valid_folder_structure, f"{bcolors.WARNING}Unexprected file "+el+"{bcolors.ENDC}")
        if el not in valid_folder_structure:
            exit_code = 1
            raise RuntimeError('')
except:
    print(f"{bcolors.WARNING}Root folder structure should not be modified (submissions go in database/LANG/EDITOR_TITLE_DATE{bcolors.ENDC}")
else:
    print(f"{bcolors.OKGREEN}Folder Structure Correct{bcolors.ENDC}")

for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
    print("Checking", file)

sys.exit(exit_code)