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

#config = import_config()
#finger_id=1
#subj_num=1


def mainPipeline(config):
    
    ###### set exp. setup #####
    finger_id = int(config['Subject']['analysis_finger'])-1
    subj_num = int(config['Subject']['subject_no'])-1
    
    config['setting']['epoch_range'] = [config['setting']['epoch_range_s'], config['setting']['epoch_range_e']]
    config['setting']['filter_band'] = [config['setting']['filter_band_e'], config['setting']['filter_band_e']]
    config['setting']['baseline'] = [config['setting']['baseline_s'], config['setting']['baseline_e']]
    ###### generate instances ######    
    prep = Prep_signal(config=config)
    uti = Utilfunc(config)
    Decoder = Model(config)
    fio = FileIO(config)
    
    ###### load data ######
    data = fio.loadBCI4()[subj_num]
    
    ##### Preprocess digit movement signal ######
    resampled_dg = prep.Rectify(prep.downsample_sig(data['train_dg']), freqs=config['setting']['Rectify_band'], 
                                btype='band', gaussian_pram=config['setting']['smooth4BCI4'])

    ##### Preprocess ECoG signals ######
    resampled_ecog = prep.downsample_sig(data['train_data'])
    if (resampled_ecog.shape[-1] < 64) and (resampled_ecog.shape[-1] >48):
        resampled_ecog = np.append(resampled_ecog, np.zeros([resampled_ecog.shape[0],2]),axis=1)
    F_value = prep.Feature_Ext_filt(resampled_ecog, standardization=True, smoothing=True)
    
    ##### Set channel labels #####
    chan = [str(i+1) for i in range(resampled_ecog.shape[1])]
    finger = ['Thumb','Index','Middle','Ring','Pinky']

    ##### create event signals from digit movements #####
    # This function is only for use BCI comp 4. (Dataset no.4)
    # If you want to use your custom dataset included event signal, substitute it to "trigger".
    trigger =prep.CreateTriggerBCI4(data['train_dg'], threshhold=0.5)
    event = trigger[:,finger_id][:,np.newaxis].T
    
    ###### create feature Epochs ######
    epR = uti.makeEpochs(resampled_ecog.T, event, chan).get_data()[:,0:-1,:]
    ep_dg = uti.makeEpochs(resampled_dg.T, event, finger).get_data()[:,0:-1,:]
    
    F_data = np.zeros((len(config['feature_freqs'].keys()),epR.shape[0],epR.shape[1],epR.shape[2]))
    for i in range(len(config['feature_freqs'].keys())):
        F_data[i,:,:,:] = uti.makeEpochs(F_value[:,:,i].T, event, ch_info=chan, 
               reference_type='Average').get_data()[:,0:-1,:]
    
#    F_data = F_dataR
    Ep_dg = ep_dg.transpose(0,2,1)[:,:,finger_id]
    
    F_data = np.reshape(F_data.transpose(1,2,0,3),[F_data.shape[1],
            F_data.shape[0]*F_data.shape[2], F_data.shape[3]])
    
    
    ##### Set training and test dataset for decoding analysis.######
    data_len= int(F_data.shape[0]*4/5)
    
    train_ecog = F_data[0:data_len,:,:]
    test_ecog = F_data[data_len:-1,:,:]

    train_dg = Ep_dg[0:data_len,:]
    test_dg = np.ravel(Ep_dg[data_len:-1,:])

    ##### Run decoding analysis ######
    weight = Decoder.Fit(train_ecog.transpose(1,0,2), train_dg, key='PLS', PLS_components=1)
    reconst_dg = Decoder.runReconst(test_ecog.transpose(1,0,2), weight =weight)
    
    ##### Evaluation and PLot #####
    reconst_dg = uti.Zscore(reconst_dg)
    test_dg = uti.Zscore(test_dg)
    pad_len = int(config['Decoding']['sliding_step'] *config['Decoding']['sample_points'])
    cc = np.round(np.corrcoef(reconst_dg[pad_len:-1],test_dg[pad_len:-1])[0,1],3)

    freqs= [config['feature_freqs'][list(config['feature_freqs'].keys())[i]] for i in range(len(config['feature_freqs'].keys()))]
    spacial_weight = np.reshape(weight[0:-1],[len(chan),len(config['feature_freqs'].keys())])
    freqs_domein= np.mean(spacial_weight,axis=0)
    spatial_domein = np.mean(spacial_weight,axis=1)
    
    freqs_score = (freqs_domein/np.sum(freqs_domein))*100
    spacial_score = (spatial_domein/np.sum(spatial_domein))*100
    reshape_score = np.reshape(spacial_score,[int(len(spacial_score)/8),8])

    #plot
    fig = plt.figure(figsize=(15, 10)) 
    gs = gridspec.GridSpec(2,2, width_ratios=[1,1]) 
    
    ax0 = plt.subplot(gs[0,0:2]) 
    ax0.plot(reconst_dg[pad_len:-1], label='Estimate from ECoG',linewidth =1.5)
    ax0.plot(test_dg[pad_len:-1], label = 'Actual Digit movement',linewidth =1.5)
    ax0.set_title('Subject no.'+str(subj_num+1)+'. Finger: '+finger[finger_id]+' Score: '+ str(np.round(cc,2)))
    ax0.set_ylabel('Finger flection (Zscore)')
    ax0.grid()
    ax0.legend()
    
    ax1 = plt.subplot(gs[1,0]) 
    ax1.plot(np.arange(len(freqs)),freqs_score, color = 'dimgray', linewidth =2.0)
    ax1.grid()
    ax1.set_title('Frequency domein contribution ratio')
    ax1.set_ylabel('Contribution ratio [%]')
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_xticks(np.arange(len(freqs)))
    ax1.set_xticklabels(freqs, rotation=60, fontsize=8)

    ax2 = plt.subplot(gs[1,1]) 
    im=ax2.pcolormesh(reshape_score,cmap='jet')
    ax2_divider = make_axes_locatable(ax2)
    cax2 = ax2_divider.append_axes("right", size="7%", pad="2%")
    cb2 = colorbar(im, cax=cax2)    

    ax2.set_yticks(np.arange(len(spacial_score)/8)+0.5)
    ax2.set_yticklabels(np.arange(len(spacial_score)/8)+1)
    ax2.set_xticks(np.arange(8)+0.5)
    ax2.set_xticklabels(np.arange(8)+1)
    ax2.set_title('Spacial Contribution ratio [%]')

    plt.show()
    
    