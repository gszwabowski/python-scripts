'''
Commentary by GLS 3/23/22
This script is used to determine the commercial availablity (via PubChem) of compounds in a .txt file exported from a MOE database.
For each smiles string in the .txt file, this script uses PubChemPy to obtain a compound ID number from the smiles string. Each ID
number is then used with BeautifulSoup to obtain XML data containing vendor information for each compound from PubChem.

PubChemPy can be installed using the directions at the following link:
https://pubchempy.readthedocs.io/en/latest/guide/gettingstarted.html

BeautifulSoup can be installed using the directions at the following link:
https://pypi.org/project/beautifulsoup4/ (use 'pip install beautifulsoup4')

lxml must be installed with 'pip install lxml' to handle XML parsing.

Inputs: a .txt file obtained by saving a MOE .mdb file as .txt, name of the field in the .mdb file containing smiles strings
Output: a table printed to the user/.csv file containing information regarding the commercial availability of all database compounds.

The .csv file resulting from this script can be imported into a MOE database and merged with the compound database based on smiles keys.

Example command: python get_compound_vendors.py input.txt mol
'''

# imports
import pubchempy as pcp
from bs4 import BeautifulSoup
import re
import urllib.request
from urllib.error import HTTPError
import sys
import time
import os

# pandas import/options
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def get_compound_vendors():
    # args from CMD
    txt_file = str(sys.argv[1])
    smiles_field = str(sys.argv[2])
    
    # read in MOE database .txt file, get smiles strings
    input_df = pd.read_csv(txt_file)
    smiles_strings = input_df[smiles_field]
    i = 1
    
    # create empty dataframe to fill with compound vendor information
    output_df = pd.DataFrame(columns = ['smiles', 'name', 'commercially_available', 'num_vendors', 'vendors'])

    for string in smiles_strings:
        print('Getting information for compound', i, '(' + string + ')')
        i += 1
        # get compound with pubchempy
        compound = pcp.get_compounds(string, 'smiles')
        # get compound number to use in BeautifulSoup URL
        num = ''
        for c in str(compound):
            if c.isdigit():
                num = num + c

        # if there is no compound ID (length of 0), name is NA. else, name is the compound's IUPAC name.
        if len(num) == 0:
            name = 'NA'
        else:
            name = compound[0].iupac_name
            
        # get XML with vendor information using the compound number
        BASE_URL = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/categories/compound/'
        URL = BASE_URL + num + '/XML/'
        try:
            source = urllib.request.urlopen(URL)
            soup = BeautifulSoup(source,'lxml')
        # exception handling for cases where no vendor info exists
        except HTTPError as err:
            if err.code == 400:
                #print('N')
                CA = 'N'
                num_vendors = 0
                dict = {'smiles': [string], 'name': [name], 'commercially_available': [CA], 'num_vendors': [num_vendors], 'vendors': ['NA']}
                df = pd.DataFrame(dict)
                output_df = pd.concat([output_df, df], ignore_index=True)
        else:
            # find vendor names, strip XML tags, store vendors
            vendors_xml = soup.find_all('sourcename')
            xml_stripped = re.sub('<[^>]*>', '', str(vendors_xml))
            vendors = xml_stripped.split(',')
            CA = 'Y'
            num_vendors = len(vendors)
            if num_vendors > 0:
                dict = {'smiles': [string], 'name': [name], 'commercially_available': [CA], 'num_vendors': [num_vendors], 'vendors' : [vendors]}
                df = pd.DataFrame(dict)
                output_df = pd.concat([output_df, df], ignore_index=True)
                
    # print table to user    
    print(output_df)
    
    #write table to csv
    output_df.to_csv(os.path.splitext(txt_file)[0] + '_CA.csv', index = False)
    print('Results written to', os.path.splitext(txt_file)[0] + '_CA.csv.\n')
 
#call main function
get_compound_vendors()