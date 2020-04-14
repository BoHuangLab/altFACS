import sys
from os.path import isfile, join
import fcsparser
import pandas as pd

def getChannelMeta(path: str)-> pd.DataFrame:
    '''strip Channel metadata from an .fcs file
    
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2892967/pdf/nihms203250.pdf
    '''
    
    meta, data = fcsparser.parse(path, reformat_meta=True)
    
    channel_metadata = meta['_channels_']
    
    channel_metadata = channel_metadata.reset_index(drop=True)
    
    channel_meta_dict = {'$PnN': 'Channel', 
                         '$PnR': 'Range', 
                         '$PnB': 'Bit Depth', 
                         '$PnE': 'Amplification Type', 
                         '$PnV': 'Voltage', 
                         '$PnG': 'Gain'}
    
    channel_metadata = channel_metadata.rename(columns=channel_meta_dict)
    
    return channel_metadata


def getFileInfo(filelist, **kwargs)->pd.DataFrame():
    '''strip some information from the input file name'''
    
    #Get **kwargs
    search_list = kwargs.get('search_list', None)
    
    file_info = pd.DataFrame()
    
    #convert to lower case
    low_files = [file.lower() for file in filelist]
    
    file_info['File']     = range(len(filelist))
    file_info['Control']  = ['control'  in file for file in low_files]
    file_info['GFP']      = ['gfp'      in file for file in low_files]
    file_info['ALFA']     = ['alfa'     in file for file in low_files]
    file_info['Snoop']    = ['snoop'    in file for file in low_files]
    file_info['Halo']     = ['halo'     in file for file in low_files]
    file_info['JF646+']   = ['jf646'    in file for file in low_files] and ['+' in file for file in low_files]
    file_info['JF646-']   = ['jf646'    in file for file in low_files] and ['-' in file for file in low_files]
    file_info['sfCherry'] = ['sfcherry' in file for file in low_files]
    file_info['LP']       = ['lp'       in file for file in low_files]
    
    #Get the landing pad Architecture
    file_info['Architecture'] = [[word for word in file.split() if 'LP' in word] for file in filelist]
    
    if search_list is not None:
        
        for term in search_list:
            file_info[term] = [term.lower() in file for file in low_files]
    
    return file_info
        
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

## Combine classifiers
def combineClassifiers(data, input_columns, output_column, drop=False):
    '''Combine mutually exclusive input_columns into a single catagorical output column.'''
    
    data[output_column] = data[input_columns].idxmax(axis=1)
    
    if drop:
        data.drop(columns=input_columns)
        
    return data

#Fix Architectures
def fixArchitecture(data, architcture_column):
    '''Handle our 'landing pad' nomenclature, e.g. LP02.'''
    
    LP_list=list()
    for LP in data[architcture_column]:
        if not LP:
            LP_list.append('LP00')
        else:
            LP_list.append(LP[0])
    
    return LP_list