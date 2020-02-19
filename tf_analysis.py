#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:36:51 2020

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


def EventRelated_BCI4(config):
    
    ###### set exp. setup #####
    finger_id = int(config['Subject']['analysis_finger'])-1
    subj_num = int(config['Subject']['subject_no'])-1

    ###### generate instances ######    
    prep = Prep_signal(config=config)
    uti = Utilfunc(config)
    fio = FileIO(config)
    
    ###### load data ######
    data = fio.loadBCI4()[subj_num]
    
    ##### Preprocess ECoG signals ######
    print(data['train_data'].shape)
    resampled_ecog = prep.downsample_sig(data['train_data'])
    if (resampled_ecog.shape[-1] < 64) and (resampled_ecog.shape[-1] >48):
        resampled_ecog = np.append(resampled_ecog, np.zeros([resampled_ecog.shape[0],2]),axis=1)
    print(resampled_ecog.shape)
    ##### Set channel labels #####
    chan = [str(i+1) for i in range(resampled_ecog.shape[1])]

    ##### create event signals from digit movements #####
    # This function is only for use BCI comp 4. (Dataset no.4)
    # If you want to use your custom dataset included event signal, substitute it to "trigger".
    trigger =prep.CreateTriggerBCI4(data['train_dg'], threshhold=0.4, gaussian_pram=[300,200])
    event = trigger[:,finger_id][:,np.newaxis].T
    
    ###### create feature Epochs ######
    epR = uti.makeEpochs(resampled_ecog.T, event, chan).get_data()[:,0:-1,:]
    time = prep.get_time()
    
    data = np.mean(epR,axis=0)
    bias=0

    plt.figure(figsize=(10,25))
    plt.tick_params(labelleft=False, labelright=False, labeltop=False,
                    left=False, right=False, top=False)

    for i in range(data.shape[0]):

        plt.plot(time,uti.Zscore(data[i,:])+bias)
        if i == data.shape[0]-1:
            plt.vlines(x=0, ymin=-10, ymax=bias, linestyle ='dashed', color = 'dimgray')
        bias=bias+10

    plt.title('Event related activity')
    plt.ylabel('Channels')
    plt.xlabel('time from onset [s]')
    plt.xlim([config['setting']['epoch_range'][0], config['setting']['epoch_range'][1]])
    plt.ylim([-10, bias+5])
    plt.show()
    
    