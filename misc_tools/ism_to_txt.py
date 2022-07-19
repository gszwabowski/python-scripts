# This script will allow a user to import convert an inactives_nM.ism file downloaded from
# a target's folder on DUD-E to .txt for use within moe. This script has been created with
# the inactives_nM.ism file in mind, so make sure to first identify the human UniProt code
# for a target and then download the inactives_nM.ism file from the DUD-E subdirectory named
# after the UniProt ID.

# Example command (from windows CMD while in directory with .ism):
# python ism_to_txt.py inactives_nM.ism

#import pandas, sys, and time modules
import pandas as pd
import sys
import time

#main function
def main():
    ism_file = sys.argv[1]
    df = pd.read_csv(ism_file, sep=" ", header=None)
    
    # drop columns that do not contain smiles, dat, activity, or uniprot code
    df.drop(list(set(df.columns) - set([0,1,2,3,4,5,8])), axis = 1, inplace = True)
    df.columns = ['smiles', 'dat', 'act1', 'act2', 'act3', 'act4', 'uniprot']
    df.insert(2, 'activity', df['act1'] + df['act2'] + df['act3'].astype('str') + df['act4'])
    df.drop(['act1', 'act2', 'act3', 'act4'], axis = 1, inplace = True)
    
    # write table to .txt
    ism_filename = ism_file.split('/')[-1]
    filename = ism_filename[:-4] + '_for_moe_import.txt'
    df.to_csv(filename, header=list(df.columns), index=None, sep=' ')
    
    print('\nDone.', ism_file, 'has been converted to', filename + '.')
#call main function
main()
