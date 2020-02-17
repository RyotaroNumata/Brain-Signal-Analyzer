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
from SignalProcessing.Wavelet import wavelet_analysis_p


class Application(Tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        self.config = import_config()
        
        quit_b = Tk.Button(self.master, text="QUIT", fg="red", command= root.destroy)
        quit_b.pack(side="bottom")
        
#        self.fig = plt.figure(figsize=(7,5))
#        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
#        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        test = Tk.Button(self.master, text="test", command= self.plot)
        test.pack(side="bottom")
        test = Tk.Button(self.master, text="update", command= self.renew_chan)
        test.pack(side="bottom")
        
        self.ch=0
        self.ret = wavelet_analysis_p(config=self.config)
        self.ret=self.ret.transpose(0,2,1)
        
    def renew_chan(self):
        self.ch = self.ch+1
        self.fig.clf()
        self.canvas.get_tk_widget().pack_forget()
        self.plot()
        
    def plot(self):
        
        self.fig = plt.figure(figsize=(7,5))
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        tf_ax = plt.axes([0.1, 0.2, 0.8, 0.5])
#        trig_ax = plt.axes([0.1, 0.15, 0.8, 0.07])
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.02])
        freqs_range = np.arange(1, 250, 5)

        # in plot_ax we plot the function with the initial value of the parameter a
        plt.axes(tf_ax) # select sin_ax
        plt.title('Time-frequency power. Ch '+str(self.ch+1))
#        print(self.ret[0,0:2000,::-1].shape)
        
        self.tf = plt.imshow(self.ret[self.ch,0:2000,::-1].T, aspect=15)
        plt.yticks(np.arange(0,50,5), freqs_range[::5][::-1])
        
        
#        data = np.random.rand(100000)
#        plt.axes(trig_ax)
#        plt.ylim(-2,2)
#        self.plot = plt.plot(data[0:2000], 'k')
#        self.plot2 = plt.plot(data[0:2000]*1.2, 'r')
#        plt.xlim(0, 2000)

        # here we create the slider
        self.a_slider = Slider(slider_ax,      # the axes object containing the slider
                          'time',            # the name of the slider parameter
                          0,          # minimal value of the parameter
                          100000,          # maximal value of the parameter
                          valinit=1  # initial value of the parameter
                         )
        
        def update(a):            
            self.tf.set_data(self.ret[self.ch,0+int(a):2000+int(a),::-1].T)
#            self.plot[0].set_ydata(data[0+int(a):2000+int(a)])
#            self.plot2[0].set_ydata(data[0+int(a):2000+int(a)]*1.2)
#            plot4.set_ydata(trigger[:,0][0+int(a):2000+int(a)]*1.5)
#            plot5.set_ydata(trigger[:,1][0+int(a):2000+int(a)]*1.8)
#            plot6.set_ydata(trigger[:,2][0+int(a):2000+int(a)]*1.5)
#            plot7.set_ydata(trigger[:,3][0+int(a):2000+int(a)]*1.8)
            self.fig.canvas.draw_idle()
        self.a_slider.on_changed(update)
        
        
root = Tk.Tk()
root.wm_title("Wavelet analysis")

app = Application(master=root)

#fig = plt.figure(figsize=(7,5))
#canvas = FigureCanvasTkAgg(fig, root)
#canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
app.mainloop()
