#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:41:04 2020

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


config = import_config()
## set analysis finger
finger_id = 4
## set subject number
subj_num =0

chan =0
###### generate instances ######    
prep = Prep_signal(config=config)
uti = Utilfunc(config)
Decoder = Model(config)
fio = FileIO(config)

###### load data ######
data = fio.loadBCI4()[subj_num]

##### Preprocess ECoG signals ######
resampled_ecog = prep.downsample_sig(data['train_data'])
resampled_dg = prep.Rectify(prep.downsample_sig(data['train_dg']), freqs=[1,10], btype='band', gaussian_pram=[200,500])

##### create event signals from digit movements #####
# This function is only for use BCI comp 4. (Dataset no.4)
# If you want to use your custom dataset included event signal, substitute it to "trigger".
trigger =prep.CreateTriggerBCI4(data['train_dg'], threshhold=0.5)

#test
freqs = prep.make_wavalet()
freqs_range = np.arange(1, 250, 5)
a =[]
for ch in range(1):
    ch = 0
    inlet = np.zeros([len(freqs), resampled_ecog.shape[0]])
    for w in range(len(freqs)):
        
        conv= np.convolve(freqs[w], resampled_ecog[:,ch], mode='valid')        
        conv = uti.Zscore((conv*conv.conj()).real)
        conv= np.append(conv, np.zeros([int(freqs[w].shape[0]/2)]))
        conv= np.append(np.zeros([int(freqs[w].shape[0]/2)+1]),conv)
        inlet[w,:]=conv[0:resampled_ecog.shape[0]]
    a.append(inlet)

resampled_ecog = a[0].T
a_min = 0    # the minimial value of the paramater a
a_max = int(resampled_ecog.shape[0]-2000)  # the maximal value of the paramater a
a_init = 1   # the value of the parameter a to be used initially, when the graph is created

root = Tk.Tk()
root.wm_title("Wavelet analysis")
root.geometry("700x600")

quit_b = Tk.Button(text="QUIT", fg="red", command= root.destroy)
quit_b.pack(side="bottom")
change_chan = Tk.Button()
change_chan["text"] = ">"
change_chan["command"] = print('test')
change_chan.pack(side="top")

fig = plt.figure(figsize=(7,5))
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

tf_ax = plt.axes([0.1, 0.2, 0.8, 0.5])
trig_ax = plt.axes([0.1, 0.15, 0.8, 0.07])
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.02])

resampled_ecog = (resampled_ecog-np.mean(resampled_ecog[0:2000,:], axis=0))
# in plot_ax we plot the function with the initial value of the parameter a
plt.axes(tf_ax) # select sin_ax
plt.title('Time-frequency power. Ch '+str(ch+1))
tf = plt.imshow(resampled_ecog[0:2000,::-1].T, aspect=15)
plt.yticks(np.arange(0,50,5), freqs_range[::5][::-1])

plt.axes(trig_ax)
plt.ylim(0,500)
plot3, = plt.plot(trigger[0:2000,4], 'k') 
plot4, = plt.plot(trigger[0:2000,0]*1.5, 'r')
plot5, = plt.plot(trigger[0:2000,1]*1.8, 'b') 
plot6, = plt.plot(trigger[0:2000,2]*1.8, 'c')
plot7, = plt.plot(trigger[0:2000,3]*1.8, 'g') 
plt.xlim(0, 2000)

# here we create the slider
a_slider = Slider(slider_ax,      # the axes object containing the slider
                  'time',            # the name of the slider parameter
                  a_min,          # minimal value of the parameter
                  a_max,          # maximal value of the parameter
                  valinit=a_init  # initial value of the parameter
                 )

def update(a):

    tf.set_data(resampled_ecog[0+int(a):2000+int(a),::-1].T)
    plot3.set_ydata(trigger[:,4][0+int(a):2000+int(a)])
    plot4.set_ydata(trigger[:,0][0+int(a):2000+int(a)]*1.5)
    plot5.set_ydata(trigger[:,1][0+int(a):2000+int(a)]*1.8)
    plot6.set_ydata(trigger[:,2][0+int(a):2000+int(a)]*1.5)
    plot7.set_ydata(trigger[:,3][0+int(a):2000+int(a)]*1.8)
    fig.canvas.draw_idle()

a_slider.on_changed(update)

Tk.mainloop()