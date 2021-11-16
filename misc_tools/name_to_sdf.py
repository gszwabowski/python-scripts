#This script will allow a user to import .sdf files from a list of common
#compound names.
#
#file should be ANSI encoded from Notepad++
#PubChemPy can be installed using the directions at the following link:
#https://pubchempy.readthedocs.io/en/latest/guide/gettingstarted.html
#
#Example command (from windows CMD while in directory with .txt):
#python name_to_sdf.py compound_names.txt

#import pubchempy, sys, and time modules
import pubchempy as pcp
import sys
import time

#main function
def main():
    i=1
    file = sys.argv[1]

    #strip quotes from line
    with open(file, 'r') as f, open('names.txt', 'w') as fo:
        for line in f:
            #line = line.lstrip('\"')
            #line = line.rstrip('\"')
            fo.write(line.replace('"', '').replace("'", ""))

    #get length of names list
    with open('names.txt', 'r') as f:
        namelist = list(f)
        l = len(namelist)


    #create empty list for compounds unable to be found
    c_list = []
    
    #write each compound's name and corresponding SMILES string to file
    with open('names.txt', 'r') as f, open('SMILES_strings.txt', 'w') as fo:
        for line in f:
            result = pcp.get_compounds(line, 'name')
            print('Downloading ' + line.rstrip() + ' SMILES string (' + str(i) + ' of ' + str(l) + ')\n')
            i=i+1
            if len(result) > 1:
                result = result[0]
                fo.write(line.rstrip())
                fo.write('\t')
                fo.write(result.isomeric_smiles + '\n')
            elif result == []:
                c_list.append(line)
            else:
                for compound in result:
                    #only write 1 SMILES string if multiple are listed since MOE will
                    #take care of stereochemistry sampling during the conf. search
                    fo.write(line.rstrip())
                    fo.write('\t')
                    fo.write(compound.isomeric_smiles + '\n')

    print("Done.\n")
    if len(c_list) > 0:
        print('SMILES strings could not be found for the following compounds:\n')
        for name in c_list:
            print(name + '\n')
#call main
main()
