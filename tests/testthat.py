import os 
import glob 
import unittest
import sys
import csv
import codecs 

exit_code = 0
error_place = ''

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
print('Testing folder structure...')
valid_folder_structure =  [".git", ".gitignore", ".github", "data", "CITATION.cff", "examples", "example_graph.png", "LICENSE", "README.md",
            "schema", "tests", "transform"]
actual_folder_structure = os.listdir('.')
folder_error = 0
for el in actual_folder_structure:
    try:
        if el not in valid_folder_structure:
            exit_code = 1
            folder_error = 1
            error_place = el
            raise RuntimeError('')
    except:
        print(f"{bcolors.FAIL}Error caused by directory <"+error_place+f">.{bcolors.ENDC}")
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
                    error_place = folder
                    raise RuntimeError('')                
            except:
                print(f"{bcolors.FAIL}Error caused by directory <"+error_place+f">.{bcolors.ENDC}")
                print(f"{bcolors.WARNING}folder names should be ISO 639 language codes (with optional + symbol for language hybrids{bcolors.ENDC}")  
                continue
if iso_error == 0:
    print(f"{bcolors.OKGREEN}Folders follow the ISO language codes{bcolors.ENDC}")

# test_that("data has correct subfolders named by ISO 639 language codes", {
#   language_codes = read.csv("iso-639-3_20200515.tab", sep = "\t")
#   observed = unique(unlist(strsplit(list.files("../../data/"), "\\+")))
#   expect_true(all(observed %in% language_codes$Id), 
#               info = "folder names should be ISO 639 language codes 
#               (with optional + symbol for language hybrids")
# })

# for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
#     print("Checking", file)


sys.exit(exit_code)