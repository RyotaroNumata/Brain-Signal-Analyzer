#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:32:55 2020

@author: numata
"""
import numpy as np
from SignalProcessing.preprocess_signal import Prep_signal
import matplotlib.pyplot as plt
from matplotlib import gridspec
from Utils.utils import Utilfunc, import_config
from Model.Decoding import Model
from FileIO.fileio import FileIO
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.axes_grid1.colorbar import colorbar
from matplotlib.widgets import Slider  # import the Slider widget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import tkinter as Tk
from joblib import Parallel, delayed

def wavelet_subfunc(freqs, data,uti):
    
    inlet = np.zeros([len(freqs), data.shape[0]])
    for w in range(len(freqs)):    
        conv= np.convolve(freqs[w], data, mode='valid')        
        conv = uti.Zscore((conv*conv.conj()).real)
        conv= np.append(conv, np.zeros([int(freqs[w].shape[0]/2)]))
        conv= np.append(np.zeros([int(freqs[w].shape[0]/2)+1]),conv)
        inlet[w,:]=conv[0:data.shape[0]]
    return inlet

def wavelet_analysis_p(config):

    subj_num = config['Subject']['subject_no']-1
    
    ###### generate instances ######    
    prep = Prep_signal(config=config)
    uti = Utilfunc(config)
    fio = FileIO(config)
    
    ###### load data ######
    data = fio.loadBCI4()[subj_num]
    
    ##### Preprocess ECoG signals ######
    resampled_ecog = prep.downsample_sig(data['train_data'])
    tg = prep.downsample_sig(data['train_dg'])
    trigger =prep.CreateTriggerBCI4(data['train_dg'], threshhold=0.5, gaussian_pram=[200,30])
    
    freqs = prep.make_wavalet()

    ret = Parallel(n_jobs=-1)(delayed(wavelet_subfunc)(freqs, resampled_ecog[:,n], uti) for n in range(resampled_ecog.shape[-1]))

    return np.asarray(ret), tg, trigger
