#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:40:04 2020

@author: numata
"""

import numpy as np
from SignalProcessing.preprocess_signal import Prep_signal
from Utils.utils import Utilfunc
from sklearn import linear_model 
from sklearn.cross_decomposition import PLSRegression


class Model(Utilfunc,Prep_signal):
    """
    Decoring class function for ECoG analysis
    -- Inheritance Utilfunc, Prep_sigal as super class
    
    Parameters
    input
        config: config json file that include parameters for analysis
    
    Note
    ----------
    The default values are defined in config
    """
    
    def __init__(self,config):
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
        
        self.sliding_step = config['Decoding']['sliding_step']
        self.sample_points = config['Decoding']['sample_points']
        
        self.srate = self.srate/float(self.dwn_rate)
    
        self.time = np.arange(self.epoch_range[0],self.epoch_range[1],1/(self.srate /self.dwn_rate))
    
    def Fit(self, ecog, emg, key='OLS',PLS_components=3):
        """
        Fit training dataset with specified method
        
        Parameters
        -----------
        ecog: array
            trainging data of ECoG.
              
        emg: array
            trainging data of EMG
        
        Return
        ----------
        ret: instance
            model instance based on regresser
        """
        
        ret =0
        if key=='OLS':
            ret=self.Linearfit(ecog, emg)
        elif key=='BaysianRidge':
            ret=self.BayesianRidgefit(ecog, emg)
        elif key == 'LASSO':
            ret = self.Lassofit(ecog, emg)
        elif key == 'PLS':
            ret = self.PLSfit(ecog, emg, PLS_components)
        else:
            assert ret!=0,str(key)+' is not mehtod in "Fit". must choose from OLS, BaysianRidge, LASSO, PLS.' 
        
        return ret
    
    def BayesianRidgefit(self, ecog, emg):
        """
        Fit training dataset to Bayesian Ridge Regression
        
        Parameters
        input
            ecog: trainging data of ECoG.
                  
            emg: trainging data of EMG
        
        Note
        ----------
        The default values are defined in config
        """
        
        self.model = linear_model.BayesianRidge()
        
        train_emg = np.ravel(emg)
        train_ecog = self.Unfolding2D(np.transpose(ecog,(1,0,2)))
        
        self.model.fit(np.abs(train_ecog), train_emg)
        
        self.WW = np.append(self.model.coef_,0)
        
        return self.WW
    
    def Linearfit(self, ecog, emg):
        """
        Fit training dataset to Linear Regression
        
        Parameters
        input
            ecog: trainging data of ECoG.
                  
            emg: trainging data of EMG
        
        Note
        ----------
        The default values are defined in config
        """
        
        self.model = linear_model.LinearRegression()
        
        train_emg = np.ravel(emg)
        train_ecog = self.Unfolding2D(np.transpose(ecog,(1,0,2)))
        
        self.model.fit(np.abs(train_ecog), train_emg)
        
        self.WW = np.append(self.model.coef_,0)
        
        return self.WW
    
    def Lassofit(self, ecog, emg):
        """
        Fit training dataset to Linear Regression
        
        Parameters
        input
            ecog: trainging data of ECoG.
                  
            emg: trainging data of EMG
        
        Note
        ----------
        The default values are defined in config
        """
        
        self.model = linear_model.Lasso()
        
        train_emg = np.ravel(emg)
        train_ecog = self.Unfolding2D(np.transpose(ecog,(1,0,2)))
        
        self.model.fit(np.abs(train_ecog), train_emg)
        
        self.WW = np.append(self.model.coef_,0)
        
        return self.WW
    
    def PLSfit(self, ecog, emg, component = 3):
        """
        Fit training dataset to Partial Least Square(PLS) regression
        
        Parameters
        input
            ecog: trainging data of ECoG.
                  
            emg: trainging data of EMG
        
        Note
        ----------
        The default values are defined in config
        """
        
        self.PLSmodel = PLSRegression(n_components=component)

        train_emg = np.ravel(emg)
        train_ecog = self.Unfolding2D(ecog.transpose(1,0,2))
        
        self.PLSmodel.fit(np.abs(train_ecog), train_emg)
        self.intercept = self.PLSmodel.y_mean_ - np.dot(self.PLSmodel.x_mean_ , self.PLSmodel.coef_)
        
        self.WW = np.append(self.PLSmodel.coef_,0)
        
        return self.WW
   
    def runReconst(self, x, weight = None, unfold = True, Abs=True, shuffle= False):
        """
        Reconstruction digit flection from ecog signals by using sliding window analysis.
        
        Parameters
        -----------
        x: array
            trainging data of ECoG.
              
        weight: 1D array [channel+1]
            regression weight calculated from Fit method

        unfold: bool
            if use non-epoch type of data, needs to switch to "False"
        abs: bool
            it control whether data for reconstruction process absolutize or not. 
        shuffle: bool
            it control wheter data shuffle temporally or not. 
        
        Return
        ----------
        Data: array
            Reconstracted finger flection signal
        """
        win = np.arange(self.sliding_step,self.sliding_step*self.sample_points,self.sliding_step)
        
        if unfold == True:
            x = Utilfunc.Unfolding2D(self,x.transpose(1,0,2))
        if shuffle == True:
            x = np.random.permutation(x)

        Data = np.zeros([x.shape[0],1])
        
        if weight is not None:
            self.WW = weight
      
        for i in range(self.sliding_step*self.sample_points, x.shape[0]):
            
            if Abs == True:
                Data[i,:] = np.sum(np.dot(np.abs(x[i-win]),self.WW[0:-1]))
            else:
                Data[i,:] = np.sum(np.dot(x[i-win],self.WW[0:-1]))

        Data = np.ravel(Data + self.WW[-1])
        Data[0:self.sliding_step*self.sample_points] = np.mean(Data[self.sliding_step*self.sample_points:-1])

        return Data
    
    
    
    