#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:46:02 2020

@author: numata
"""

import tkinter as tk
from Utils.utils import import_config
from Pipeline import mainPipeline

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        
        self.config = import_config()
        self.create_widgets()
        
        self.keys= []
        self.type_holder = []
        keys=list(self.config['setting'].keys())
        self.tex_instances = self.config['setting'].copy()
        
        self.keys2 = []
#        self.type_holder2 = []
        keys2= list(self.config['feature_freqs'].keys())
        self.test = keys2
        self.tex_instances2 = self.config['feature_freqs'].copy()

        self.keys3 = []
#        self.type_holder3 = []
        keys3= list(self.config['Decoding'].keys())        
        self.tex_instances3 = self.config['Decoding'].copy()
        
        self.keys4 = []
#        self.type_holder4 = []        
        keys4= list(self.config['Subject'].keys())
        self.tex_instances4 = self.config['Subject'].copy()

        for k in range(len(list(self.config['setting'].keys()))):
            if (type(self.config['setting'][keys[k]]) == list)==True:
                ret=self.create_textbox(self.config['setting'][keys[k]][0], label=keys[k])
                
                self.tex_instances[keys[k]+'_s'] = ret
                self.keys.append(keys[k]+'_s')
                self.type_holder.append('float')
                
                ret=self.create_textbox(self.config['setting'][keys[k]][1], label=keys[k])
                self.tex_instances[keys[k]+'_e'] = ret
                self.keys.append(keys[k]+'_e')
                self.type_holder.append('float')
                
            elif (type(self.config['setting'][keys[k]]) == int)==True:
#                print(keys[k])
                ret=self.create_textbox(float(self.config['setting'][keys[k]]), label=keys[k])
                self.tex_instances[keys[k]] = ret
                self.keys.append(keys[k])
                self.type_holder.append('float')
            else:
                ret=self.create_textbox(self.config['setting'][keys[k]], label=keys[k])
                self.tex_instances[keys[k]] = ret
                self.keys.append(keys[k])
                self.type_holder.append('str')
        
        for k in range(len(list(self.config['feature_freqs'].keys()))):

                self.keys2.append(keys2[k]+'_s')
                self.keys2.append(keys2[k]+'_e')

        for k in range(len(list(self.config['Decoding'].keys()))):
  
                ret=self.create_textbox(float(self.config['Decoding'][keys3[k]]), label=keys3[k])
                self.tex_instances3[keys3[k]] = ret
                self.keys3.append(keys3[k])
                
        for k in range(len(list(self.config['Subject'].keys()))):
  
                ret=self.create_textbox(float(self.config['Subject'][keys4[k]]), label=keys4[k])
                self.tex_instances4[keys4[k]] = ret
                self.keys4.append(keys4[k])
            
    def create_widgets(self):

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Run analysis"
        self.hi_there["command"] = self.runDecoding
        self.hi_there.pack(side="top")

        self.update = tk.Button(self)
        self.update["text"] = "select feature"
        self.update["command"] = self.freq_window
        self.update.pack(side="top")
        
        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

    def create_textbox(self, data, window=None,label='TEST'):
        
        if window is None:
            self.textbox = tk.Entry()
            self.textbox.insert(tk.END, data)
            label = tk.Label(text=label)
            label.pack(padx=100, pady=1, anchor=tk.W)
            self.textbox.pack(padx=100, pady=1, anchor=tk.W)
        else:
            self.textbox = tk.Entry(window)
            label = tk.StringVar()
            label.set('Feature freqs: ')
            label = tk.Label(window, textvariable=label)

            self.freqslabel.append(label)
            label.pack(padx=5, pady=5, anchor=tk.W)
            self.textbox.insert(tk.END, data)
            self.textbox.pack(padx=5, pady=5, anchor=tk.W)
        
        return self.textbox

    def freq_window(self):
        self.window_param =[]
        self.freqslabel=[]
        self.count = 0
        self.window = tk.Toplevel()
        self.window.title('Entry features')

        add_param = tk.Button(self.window)
        add_param["text"] = "+"
        add_param["command"] = self.addlabel
        add_param.pack(side="top")
        add_param = tk.Button(self.window)
        add_param["text"] = "-"
        add_param["command"] = self.remlabel
        add_param.pack(side="top")
        add_param = tk.Button(self.window)
        add_param["text"] = "save"
        add_param["command"] = self.clslabel
        add_param.pack(side="top")

    def addlabel(self):
#        print(len(list(self.config['feature_freqs'].keys())), self.count)
        if self.count <= len(self.test):
                if self.count < len(list(self.config['feature_freqs'].keys())):
                        ret=self.create_textbox(self.test[self.count]+','+str(self.config['feature_freqs'][self.test[self.count]][0])+','+
									str(self.config['feature_freqs'][self.test[self.count]][1]), self.window)
                else:
                        print('add new feature')
                        ret=self.create_textbox('name, 0, 1', self.window)				
                self.window_param.append(ret)
                self.count = self.count +1
        
    def remlabel(self):
        if len(self.window_param)>0:
                print('remove feature')
                self.window_param[-1].destroy()
                del self.window_param[-1]
                self.freqslabel[-1].pack_forget()
                del self.freqslabel[-1]
                self.count = self.count -1

#        print('rm: ', len(self.window_param), len(self.freqslabel))
        
    def clslabel(self):
        print('save frequency parameter')
#        self.test = []
        freqs={}
        for i in range(len(self.window_param)):
            band_freqs = self.window_param[i].get().split(",")
            freqs[band_freqs[0]] = [float(band_freqs[1]), float(band_freqs[2])]
#            self.test.append(str(i+1))
                
        self.config['feature_freqs'] = freqs
#        print(self.config['feature_freqs'])
        self.window_param =[]
        self.conunt = 0
        self.window.destroy()
            
    def runDecoding(self):
        self.Update()
#        print(self.config)
        mainPipeline(self.config)
        
    def Update(self):

        for ins in range(len(self.keys)):
            if self.type_holder[ins] == 'float':
                self.config['setting'][self.keys[ins]] = int(float(self.tex_instances[self.keys[ins]].get()))
            elif self.type_holder[ins] == 'str':
                self.config['setting'][self.keys[ins]] = self.tex_instances[self.keys[ins]].get()
        
        self.config['setting']['epoch_range'] = [float(self.config['setting']['epoch_range_s']), float(self.config['setting']['epoch_range_e'])]
        self.config['setting']['filter_band'] = [float(self.config['setting']['filter_band_s']), float(self.config['setting']['filter_band_e'])]
        self.config['setting']['baseline'] = [float(self.config['setting']['baseline_s']), float(self.config['setting']['baseline_e'])]
        self.config['setting']['Rectify_band'] = [float(self.config['setting']['Rectify_band_s']), float(self.config['setting']['Rectify_band_e'])]
        self.config['setting']['smooth4BCI4'] = [float(self.config['setting']['smooth4BCI4_s']), float(self.config['setting']['smooth4BCI4_e'])]

        
        for ins in range(len(self.keys3)):
            self.config['Decoding'][self.keys3[ins]] = int(float(self.tex_instances3[self.keys3[ins]].get()))

        for ins in range(len(self.keys4)):
            self.config['Subject'][self.keys4[ins]] = int(float(self.tex_instances4[self.keys4[ins]].get()))
        
root = tk.Tk()
root.title('Decoding anlysis')
root.geometry("400x900")
app = Application(master=root)
app.mainloop()