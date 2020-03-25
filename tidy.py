import sys
from os.path import isfile, join
import fcsparser
import pandas as pd

def makeDataFrame(input_directory, filelist, **kwargs)->pd.DataFrame():
    '''accept a list of .fcs files and generate a tidy pandas.Dataframe'''
    
    ##Rationale users may have a single file that they want a plot from as quickly as possible.
    
    ##Converting .fcs files to pandas DataFrames allows rapid plotting and analysis with standard libraries
    
    ##Optional renaming of fluorescence channels by wavelength or by fluorophore simplifies labelling of axes, gates, etc. downstream.
    
    # This script should 
    
    #Get **kwargs
    #Information to be added for each file
    filename_dict     = kwargs.get('filename_dict', None)
    
    #Information relevant to each channel
    channel_name_dict = kwargs.get('channel_name_dict', None)
    verbose           = kwargs.get('verbose', False)
       
    if type(filelist)== str:
        
        if verbose:
            print('Generating DataFrame from one file')
        
        ##Get data from file
        path = input_directory+filelist
        meta, data = fcsparser.parse(path, reformat_meta=True)
        output = data
    
    elif type(filelist)== list:
        
        output=list()
    
        #Get data from each file in the list
        for n in range(len(filelist)):
                       
            path = input_directory+filelist[n]
            meta, data = fcsparser.parse(path, reformat_meta=True)

            #... if there is a dictionary to add info, use that
            if (filename_dict is not None):

                if verbose:
                    print('Adding file information from dictionary')
                    
                for n, column in enumerate(filename_dict[file].columns):
                    data.insert(loc=n, column=column, value = filename_dict[file].values[0][n])

            else:
                
                if verbose:
                    print('Indexing input file',n)
                    
                #Add a column to distinguish data from different files
                data.insert(loc=0, column='File', value = n)

            #Add the data to the output dataframe
            output.append(data)
            
        #Concatenate data from all files
        output = pd.concat(output)
            
    if (channel_name_dict is not None):
        
        if verbose:
            print('Renaming columns according to channel_name_dict')
                
        #Rename columns
        output.rename(columns = channel_name_dict, inplace=True)
        
    return output