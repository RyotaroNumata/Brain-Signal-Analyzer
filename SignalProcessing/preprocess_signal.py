#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:51:28 2020

@author: numata
"""

#import os
#import time
import numpy as np
from scipy import signal
from scipy.stats import norm
from mne.time_frequency import tfr_array_stockwell
import mne
from sklearn.preprocessing import StandardScaler



class Prep_signal:
    """
    Preprocessing data class for analysis.
    """


    def __init__(self,config):
        """
        Parameters
        ----------
        config: dict
            analysis config flie
        """        
        
        self.srate = config['setting']['srate']
        self.dwn_rate = config['setting']['dwn_rate']
        self.filter_order = config['setting']['filter_order']
        self.path = config['setting']['data_path']

        self.event_id = config['setting']['event_id']
        self.reference_type = config['setting']['reference_type']
        self.epoch_range = config['setting']['epoch_range']
        self.baseline = config['setting']['baseline']
        self.filter_band = config['setting']['filter_band']
        self.feature_freqs = config['feature_freqs']
        self.smooth = config['setting']['smoothing']
        
        self.srate = self.srate/float(self.dwn_rate)
    
        self.time = np.arange(self.epoch_range[0],self.epoch_range[1],1/(self.srate /self.dwn_rate))
        
    def downsample_sig(self,x):
        """downsample the data.

        Parameters
        ----------
        x : {array-like, sample × index}.
            data for downsampling. 
        Returns
        ----------
        x : downsampled data :numpy-array
        """
        return x[::self.dwn_rate,:]

    def get_time(self):
        """get time data.

        Returns
        ----------
        time: time data :numpy-array
        """
        return self.time
    
    def filter_signal(self,x, low, high):
        """bandpass filtering to input data.
        
        Parameters
        ----------
        x : {array-like, sample × index}.
            data to filtering. 
        low : int
            cuttoff frequency along low side
        high : int
            cuttoff frequency along high side
        Returns
        ----------
        x: filtered signals :numpy-array
        """

        ## set filtering parameters
        low = low / (self.srate/2.)
        high = high / (self.srate/2.)
        b_filt, a_filt = signal.iirfilter(self.filter_order, [low, high], btype = 'band')


        return signal.filtfilt(b_filt, a_filt, x, axis=0)
    
    
    def Rectify(self, x, freqs = [4], btype='lowpass', gaussian_pram =[200,200]):
        """Rectify data.
        
        Parameters
        ----------
        x : {array-like, sample × index}.
            data to rectify. 
        freqs : list
            cuttoff frequency along low side.
            if you want to use banndpass filter, freqs needs two filtering values in list [low, high]. 
        btype : str
            type of filtering. default is lowpass.
        gaussian_pram: list
            parameter for smoothing.
        
        Returns
        ----------
        X: Rctified siganls :numpy-array
        """        
        
        if (btype == 'lowpass') & (len(freqs)==1):
            
            low = freqs[0] / (self.srate/2.)        
            b_filt, a_filt = signal.iirfilter(self.filter_order, low, btype = 'lowpass')
        
        elif (btype == 'band') & (len(freqs)==2):
            
            low = freqs[0] / (self.srate/2.)
            high = freqs[1] / (self.srate/2.)
            b_filt, a_filt = signal.iirfilter(self.filter_order, [low, high], btype = 'band')            
        
        X = signal.filtfilt(b_filt, a_filt, x, axis=0)
        
        X=self.GaussianWin2(np.abs(X),gaussian_pram)
        
        return X

    def Feature_Ext_filt(self,x, standardization=True, smoothing=True):
        """Feature extraction from signals.
        
        Parameters
        ----------
        x : {array-like, sample × index}.
            ecog data. 
        standardization: bool
            if it's True, standardize feature siganls.
        smoothing: bool
            if it's True, do smoothing to feature siganls with lowpass filter.           
        
        Returns
        ----------
        Data: feature matrix {array-like}
             sample × channels× feature
        """          
        if x.shape[0] < x.shape[1]:
            x=x.T
        
        freqs_list = list(self.feature_freqs.keys())
        
        print('####### Filtering for feature extraction ######',len(freqs_list),'band')
        if standardization is not False:
              print('standardization : ON')
        
        Data = np.zeros((x.shape[0],x.shape[1],len(freqs_list)))
        
        for i in range(len(freqs_list)):
            
             fband= self.feature_freqs[str(freqs_list[i])]
             
             X = np.abs(self.filter_signal(x,fband[0],fband[1]))
             print('Band-pass filtering (Zero-phase):',fband[0],'Hz to',fband[1],'Hz (',str(freqs_list[i]),')')

             if smoothing == True:
                 print("### Processing smoothing ###")
                 low = self.smooth / (self.srate/2.)        
                 b_filt, a_filt = signal.iirfilter(self.filter_order, low, btype = 'lowpass')
                 X = signal.filtfilt(b_filt, a_filt, X, axis=0)
  
             if standardization is True:
                 
                 scaler = StandardScaler()                 
                 Data[:,:,i] = scaler.fit_transform(X)
             else:
                 Data[:,:,i] = X

        return Data


    def GaussianWin2(self, x, param):
        """smoothing with Gaussian window.
        
        Parameters
        ----------
        x : {array-like, sample × index}.
            data. 
        param: list
            parametr of gaussian distribution. it needs to contain two values. [mean, variance]   
        
        Returns
        ----------
        X: smoothed siganls {array-like}
           sample × channels
        """                 
        if x.shape[0] < x.shape[1]:
            x=x.T
        
        win_len= param[0]
        win_var= param[1]
        
        window = norm.pdf(np.arange(win_len), loc=int(win_len/2), scale=win_var)
        X = np.zeros([x.shape[0],x.shape[1]])
         
        for i in range(x.shape[1]):
            X[:,i] = np.convolve(window/window.sum(), x[:,i], mode='same')

        return X
    
    def CreateTriggerBCI4(self,data, threshhold=0.5, gaussian_pram =[200,200]):
        """Create tirigger signals base on digit flection movement.
        
        Parameters
        ----------
        x : {array-like, sample × index}.
            finger flection data. 
        
        threshhold: int
            it use to estimate cue onset.
        
        gaussian_pram: list
            smoooothing parameter [mean, variance]
        
        Returns
        ----------
        trigger: estimated trigger siganls {array-like}
        """             
        trigger = self.Rectify(self.downsample_sig(data), freqs=[1,10],btype='band')        
        trigger[trigger < threshhold] =0
        trigger[trigger > 0] = self.event_id
        
        return trigger
    
    