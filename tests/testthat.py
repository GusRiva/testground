import os 
import glob 
import sys
import re 
import csv
import codecs 
from lxml import etree as et 
import networkx as nx
# import pydot 

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

#FOLDER STRUCTURE
print(f"{bcolors.HEADER}Testing folder structure...{bcolors.ENDC}")
print('Check root folders and files...')
valid_folder_structure =  [".git", ".gitignore", ".github", "data", "CITATION.cff", "examples", "example_graph.png", "LICENSE", "README.md",
            "schema", "tests", "transform"]
actual_folder_structure = os.listdir('.')
folder_error = 0
for el in actual_folder_structure:
    try:
        if el not in valid_folder_structure:
            exit_code = 1
            folder_error = 1
            raise RuntimeError('')
    except:
        print(f"{bcolors.FAIL}Error caused by directory <"+el+f">.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}Root folder structure should not be modified (submissions go in database/LANG/EDITOR_TITLE_DATE{bcolors.ENDC}")
        continue
if folder_error == 0:
    print(f"{bcolors.OKGREEN}Folder Structure Correct{bcolors.ENDC}")

# ISO language codes
print("Checking if data has correct subfolders named by ISO 639 language codes")
iso_error = 0
with codecs.open('./tests/testthat/iso-639-3_20200515.tab', 'r', 'utf-8') as isos:
    language_codes = list(csv.reader(isos, delimiter = "\t"))
    language_codes = [x[0] for x in language_codes]
    for folder in os.listdir('data'):
        for part in folder.split('+'):
            try:
                if part not in language_codes:
                    exit_code = 1
                    iso_error = 1
                    raise RuntimeError('')                
            except:
                print(f"{bcolors.FAIL}Error caused by directory <"+folder+f">.{bcolors.ENDC}")
                print(f"{bcolors.WARNING}folder names should be ISO 639 language codes (with optional + symbol for language hybrids{bcolors.ENDC}")  
                continue
if iso_error == 0:
    print(f"{bcolors.OKGREEN}Folders follow the ISO language codes{bcolors.ENDC}")

# FOLDER NAMING
print("Checking that subsubfolders are named consistently (FirstEditorLastName_Date_TitleWord)")
folders = [os.path.basename(x) for x in glob.iglob('data/*/*')]
folder_name_error = 0
for folder in folders:
    try:
        match= re.match('\w+_\d{1,4}[a-z]?_', folder)
        if match is None:
            folder_name_error = 1
            exit_code = 1
            raise RuntimeError('')
    except:
        print(f"{bcolors.FAIL}Error caused by directory <"+folder+f">.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}The subfolders should be named according to the structure: FirstEditorLastName_Date_TitleWord{bcolors.ENDC}")  
        continue
if folder_name_error == 0:
    print(f"{bcolors.OKGREEN}Subfolder are well constructed{bcolors.ENDC}")    

# SUBMISSIONS COMPLETE
print("Checking all submissions are complete")
completeness_error = 0
minimal_structure = ["stemma.gv", "metadata.txt"]
maximal_structure = minimal_structure + ['stemma.graphml', 'stemma.png']
folders = glob.glob('data/*/*')
for folder in folders:
    try:
        folder_base = os.path.basename(folder)
        maximal_structure += [folder_base + '.tei.xml']
        actual_structure = []
        for file in glob.glob(folder+'/*'):
            file_base = os.path.basename(file)
            actual_structure.append(file_base)
        if set(minimal_structure).issubset(actual_structure) == False:
            completeness_error = 1
            exit_code = 1
            raise RuntimeError('')
        if set(actual_structure).issubset(maximal_structure) == False:
            error_file = set(actual_structure) - set(maximal_structure)
            completeness_error = 2
            exit_code = 1
            raise RuntimeError('')
    except:
        print(f"{bcolors.FAIL}Error caused by <"+folder+f">.{bcolors.ENDC}")
        if completeness_error == 1:
            print(f"{bcolors.WARNING}Missing stemma.gv or metadata.txt{bcolors.ENDC}")
        elif completeness_error == 2:
            print(f"{bcolors.WARNING}The name of the file(s) <"+' '.join(error_file)+f"> is not allowed{bcolors.ENDC}")
        continue
if completeness_error == 0:
    print(f"{bcolors.OKGREEN}All submissions are complete{bcolors.ENDC}")   

# TEI FILES
print("Checking TEI files are valid")
xmlschema_doc = et.parse('schema/openStemmata.xsd')
xmlschema = et.XMLSchema(xmlschema_doc)
validation_error = 0
for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
    try:
        tree = et.parse(file)
        xmlschema.assertValid(tree)
    except Exception as e:
        exit_code = 1
        validation_error = 1
        print(f"{bcolors.FAIL}Error caused by "+file+f".{bcolors.ENDC}")
        print(e)
        print('\n')
        continue
if validation_error == 0:
    print(f"{bcolors.OKGREEN}All TEI files are valid{bcolors.ENDC}")  
    print('\n')

# DOT FILES
print("Checking DOT files are valid")
for file in glob.iglob('./data/*/*aeus/*.gv', recursive=True):
    try:
        with codecs.open(file, 'r', 'utf-8') as dot:
            lines = '\n'.join([re.sub('#.+', '', x) for x in dot.readlines()])
            lines = re.sub('^\s+', '', lines)
            lines = re.sub('\s*$', '', lines)
            lines = re.sub(r'[^\S\r\n]+', ' ', lines)
            if lines[:9] != 'digraph {':
                raise RuntimeError('Graph should start with "digraph {"')
            if lines[-1:] != '}':
                raise RuntimeError('Graph should end with "}"')
            for line in lines.split('\n'):
                if line.isspace():
                    continue
                elif re.match('digraph\s*{', line):
                    continue
                elif re.match('\s*[\w\d]+\s+-[->]\s+[\w\d]+', line):
                    # parse attributes in square brackets
                    # print(line)
                    continue
                elif re.match('\s*[\w\d]+', line):
                    # parse attributes
                    print(line)
                    continue
                
    except Exception as e:
        print(f"{bcolors.FAIL}Error caused by "+file+f".{bcolors.ENDC}")
        print(e)
        print('\n')
        exit_code = 1

sys.exit(exit_code)