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
    verbose           = kwargs.get('verbose', False)
    
    #Information to be added for each file
    filename_info     = kwargs.get('filename_info', None)
    
    #Information relevant to each channel
    channel_name_dict = kwargs.get('channel_name_dict', None)
   
    reorder_wavelengths = kwargs.get('reorder_wavelengths', True)
       
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

            #Add a column to distinguish data from different files
            data.insert(loc=0, column='File', value = n)
            
            #Add the data to the output dataframe
            output.append(data)
            
        #Concatenate data from all files
        output = pd.concat(output)
        
    #... if there is a DataFrame to add info, use that
    if (filename_info is not None):

        if verbose:
            print('Adding file information from file_info')
                    
            output = filename_info.merge(output, how='right')
    
    if (channel_name_dict is not None):
        
        if verbose:
            print('Renaming columns according to channel_name_dict')
                
        #Rename columns
        output.rename(columns = channel_name_dict, inplace=True)
    
    if reorder_wavelengths:
        
        if verbose:
            print('Reordering columns according to wavelength')
            
        #[1] Get column labels as a series
        cols = pd.Series(output.columns)
        
        #[2] Get positions of wavelength labels
        wavelengths = ['nm' in label for label in cols]
        
        #[3] Sort the wavelength labels
        new_order = sorted(cols[wavelengths])
        
        #[4] Reorder the wavelength labels
        cols.loc[wavelengths] = new_order
        
        #[5] Reorder DataFrame Columns
        output = output.loc[:, cols]
    
    return output