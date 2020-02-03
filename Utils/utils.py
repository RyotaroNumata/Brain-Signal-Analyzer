#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:12:07 2020

@author: numata
"""

import numpy as np
import mne
import json
import os

def import_config():
    """import coonfig file.
     
    Returns
    ----------
    config : dict
        config data for analysis
    """

    config_path = os.getcwd()+'/config.json'

    with open(config_path) as f:
        config = json.load(f)
      
    return config

class Utilfunc():
    """
    Utility class function for Decoding analysis
    
    Parameters
    ----------
    input
        config: config json file that include parameters for analysis
    
    Note
    ----------
    The default values are defined in config
    """
    
    def __init__(self,config):
        self.path = config['setting']['data_path']
        self.srate = config['setting']['srate']
        self.dwn_rate = config['setting']['dwn_rate']
        self.filter_order = config['setting']['filter_order']
        self.event_n = config['setting']['event_id']
        self.reference_type = config['setting']['reference_type']
        self.epoch_range = config['setting']['epoch_range']
        self.baseline = config['setting']['baseline']
   
    def Zscore(self, X):
        """Standardize the data with mean and variance.

        Parameters
        ----------
        X : array-like, sample × index.
            input data. 
        Returns
        ----------
        ret :numpy-array
            Zscored data
        """        
        
        mu = np.mean(X, axis=0)
        std = np.std(X, axis=0)
        
        self.scaleing_param = [mu, std]
        
        ret = (X - mu) / std

        return ret
    
    def Unfolding2D(self,X):
        """Unfolding matrix 3D data to 2D data anlong specified axis.

        Parameters
        ----------
        X : array-like, 3D data.
            input data. 
        Returns
        ----------
        Flat_data :numpy-array, 2D data
            unfloding data
        """   
        
        Flat_data = np.zeros([X.shape[0]*X.shape[2],X.shape[1]])
        
        for i in range(X.shape[1]):
            data = np.ravel(X[:,i,:])
            Flat_data[:,i]=data
        
        return Flat_data   
    
    def makeEpochs(self, x, event, ch_info, baseline_correct= True, reference_type = None):
        """create epochs in MNE format.

        Parameters
        ----------
        x : array-like.
            input data sample * channels.
        event : array
            trigger signal for epoching.
        ch_info : str
            channel infomation like label of electrode.
        baseline_correct: bool
            if it's Ture, apply baseline correction.
        reference_type: str
            if it's "Average", apply common average reference (CAR) is used for analysis.
        
        Returns
        ----------
        epoch: MNE epoch format
        
        """   
        if x.shape[1] < x.shape[0]:
            x=x.T
            
        if reference_type == 'Normal':
            self.reference_type ='Normal'
            print('###### Reference type: normal #######')
        else:
            self.reference_type = 'Average'
        
        x = np.append(x,event,axis=0).T
        
        # Initialize an info structure        
        self.info = mne.create_info(
            ch_names=ch_info+ ['stim'],
            ch_types=['eeg' for i in range(x.shape[1]-1)] + ['stim'],
            sfreq=self.srate
        )

        self.event_id = {'Rest': self.event_n}
        self.raws = mne.io.RawArray(x.T,self.info)
        self.events = mne.find_events(self.raws)

        self.picks_ecog = mne.pick_types(self.info, meg=False, eeg=True, eog=False, stim=True, exclude='bads')
        
        if self.reference_type == 'Average':

            raws = self.raws.set_eeg_reference('average')
            print('###### Ecog signal are re-referenced by CAR #######')
        else:
            raws=self.raws

        if baseline_correct == True:
            self.epochs = mne.Epochs(raws, self.events, picks=self.picks_ecog, event_id=self.event_id, 
                                     proj=False, tmin=self.epoch_range[0], tmax=self.epoch_range[1], baseline=(self.baseline[0],self.baseline[1]))
        else:
            self.epochs = mne.Epochs(raws, self.events, picks=self.picks_ecog, event_id=self.event_id, 
                                     proj=False, tmin=self.epoch_range[0], tmax=self.epoch_range[1],baseline=(None))

 
        return self.epochs
    
    