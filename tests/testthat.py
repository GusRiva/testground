import os 
import glob 
import sys
import re 
import csv
import codecs 

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
        continue
if folder_name_error == 0:
    print(f"{bcolors.OKGREEN}Subfolder are well constructed{bcolors.ENDC}")    

# for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
#     print("Checking", file)


sys.exit(exit_code)