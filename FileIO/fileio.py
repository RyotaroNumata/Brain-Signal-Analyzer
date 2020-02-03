#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 19:06:03 2020

@author: numata
"""

from scipy import io
from glob import glob

class FileIO:
    """
    File input and output class
    
    Parameters
    ----------
    input
        config: config json file that include parameters for analysis
    
    Note
    ----------
    The default values are defined in config
    """
    
    def __init__(self,config):
        """
        Parameters
        ----------
        config: dict
            analysis config flie
        """        

        self.data_path = config['setting']['data_path']
        
    
    def loadBCI4(self):
        """
        Parameters
        ----------
        inlet: dict.
            loaded data.
        """        
        
        dir_list = glob(self.data_path+'*.mat')
        inlet=[]
        for i in range(len(dir_list)):
            
            inlet.append(io.loadmat(dir_list[i]))
        
        return inlet