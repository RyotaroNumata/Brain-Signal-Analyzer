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
#        quit_b.grid(column=0,row=0)
        
        test = Tk.Button(self.master, text="Drew fig", command= self.plot)
        test.pack(side="top")
        
        test = Tk.Button(self.master, text=">", command= self.renew_chan)
#        test.grid(column=1,row=0)
        test.pack(side="bottom")
        test = Tk.Button(self.master, text="<", command= self.back_chan)
        test.pack(side="bottom")
#        test.grid(column=0,row=1)
        test = Tk.Button(self.master, text="finger+", command= self.chang_trig)
        test.pack(side="bottom")
        
        test = Tk.Button(self.master, text="finger-", command= self.chang_trig_m)
        test.pack(side="bottom")
        
        self.ch=0
        self.fing = 0
        self.ret, self.trig, self.test = wavelet_analysis_p(config=self.config)
        self.ret=self.ret.transpose(0,2,1)
        
    def renew_chan(self):
        if self.ch < self.ret.shape[0]-1:
            self.ch = self.ch+1
            self.fig.clf()
            self.canvas.get_tk_widget().pack_forget()
            self.plot()
        
    def back_chan(self):
        if self.ch >0:
            self.ch = self.ch-1
            self.fig.clf()
            self.canvas.get_tk_widget().pack_forget()
            self.plot()

    def chang_trig(self):
#        print(self.fing, self.trig.shape[1]-1)
        if self.fing <self.trig.shape[1]-1:
            self.fing = self.fing+1
            self.fig.clf()
            self.canvas.get_tk_widget().pack_forget()
            self.plot()

    def chang_trig_m(self):
#        print(self.trig.shape)
        if self.fing >0:
            self.fing = self.fing-1
            self.fig.clf()
            self.canvas.get_tk_widget().pack_forget()
            self.plot()
        
    def plot(self):
        
        self.fig = plt.figure(figsize=(5,3))
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        tf_ax = plt.axes([0.1, 0.15, 0.8, 0.9])
        trig_ax = plt.axes([0.1, 0.15, 0.8, 0.07])
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.02])
        freqs_range = np.arange(1, 250, 5)

        # in plot_ax we plot the function with the initial value of the parameter a
        plt.axes(tf_ax) # select sin_ax
        plt.title('Time-frequency power. Ch '+str(self.ch+1))
#        print(self.ret[0,0:10000,::-1].shape)
#        t=np.append(np.zeros([1000,50]),np.ones([1000,50]),axis=0)
        self.tf = plt.imshow(self.ret[self.ch,0:10000,::-1].T, aspect=70)
        plt.yticks(np.arange(0,50,5), freqs_range[::5][::-1])
        plt.ylabel('Frequency [Hz]')
#        plt.xticks(np.arange(10000)[::100],np.arange(0,4,1/500)[::100])
        
        colors=["#E00010", "#F39800", "#009944", "#00A0E9", "#1D2088"]
        plt.axes(trig_ax)
#        plt.ylim(-2,2)
        self.trig_plot=[]
        
#        for i in range(1):
#            p=plt.plot(self.trig[0:10000,self.fing]*(1+(i/5)), color=colors[i])
#            self.trig_plot.append(p)
            
        self.p=plt.plot(self.trig[0:10000,self.fing], color=colors[0])
        self.p2=plt.plot(self.test[0:10000,self.fing], color=colors[1])
#        self.plot2 = plt.plot(data[0:10000]*1.2, 'r')
        plt.xlim(0, 10000)
        plt.ylim(-3,5)

        # here we create the slider
        self.a_slider = Slider(slider_ax,  # the axes object containing the slider
                          'time',          # the name of the slider parameter
                          0,               # minimal value of the parameter
                          self.ret[0,:,0].shape[0],       # maximal value of the parameter
                          valinit=0      # initial value of the parameter
                         )
        
        def update(a):
            self.tf.set_data(self.ret[self.ch,0+int(a):10000+int(a),::-1].T)
            self.p[0].set_ydata(self.trig[0+int(a):10000+int(a),self.fing])
            self.p2[0].set_ydata(self.test[0+int(a):10000+int(a),self.fing])
#            self.tf.set_label(np.arange(a, a+4, 1/self.srate))
#            for i in range(1):
#                
#                self.trig_plot[i][0].set_ydata(self.trig[0+int(a):10000+int(a),self.fing]*(1+(i/5)))
#            self.plot2[0].set_ydata(data[0+int(a):10000+int(a)]*1.2)
#            plot4.set_ydata(trigger[:,0][0+int(a):10000+int(a)]*1.5)
#            plot5.set_ydata(trigger[:,1][0+int(a):10000+int(a)]*1.8)
#            plot6.set_ydata(trigger[:,2][0+int(a):10000+int(a)]*1.5)
#            plot7.set_ydata(trigger[:,3][0+int(a):10000+int(a)]*1.8)
            self.fig.canvas.draw_idle()
        self.a_slider.on_changed(update)
        
        
root = Tk.Tk()
root.wm_title("Wavelet analysis")
root.geometry('900x700')

app = Application(master=root)

#fig = plt.figure(figsize=(7,5))
#canvas = FigureCanvasTkAgg(fig, root)
#canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
app.mainloop()
