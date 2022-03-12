import os 
import glob 
import unittest
import sys
import csv

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
try:
    for el in actual_folder_structure:
        # unittest.assertIn(el, valid_folder_structure, f"{bcolors.WARNING}Unexprected file "+el+"{bcolors.ENDC}")
        if el not in valid_folder_structure:
            exit_code = 1
            error_place = el
            raise RuntimeError('')
except:
    print(f"{bcolors.FAIL}Error caused by directory '"+error_place+"'.{bcolors.ENDC}")
    print(f"{bcolors.FAIL}Root folder structure should not be modified (submissions go in database/LANG/EDITOR_TITLE_DATE{bcolors.ENDC}")
else:
    print(f"{bcolors.OKGREEN}Folder Structure Correct{bcolors.ENDC}")

# ISO language codes
print("Checking if data has correct subfolders named by ISO 639 language codes")
try:
    with open('./tests/testthat/iso-639-3_20200515.tab') as isos:
        language_codes = csv.reader("isos", delimiter = "\t")
        for folder in os.listdir('data'):
            print(folder)
except:
    print(f"{bcolors.FAIL}Error caused by directory '"+error_place+"'.{bcolors.ENDC}")
else:
    print(f"{bcolors.OKGREEN}Folder Structure Correct{bcolors.ENDC}")

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