import tkinter as tk, re
import pandas as pd
from tkinter import messagebox as msg, filedialog as fd
from datetime import date
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from win32com.client import Dispatch

#/home/abdul/Documents/Python/Speed-Log-Extractor/table.html


class myClass(tk.Frame):       
    def __init__(self,parent):
        super().__init__(parent)
        #create an entry widget
        self.parent = parent
        self.parent.title('Create Log Speed Excel sheet from URL')
        
        self.e = tk.Entry(parent,width=100) #using self.master produces text
        self.e.grid(row=1, column=1,pady=10)

        self.btns_frame = tk.Frame(parent)
        self.btns_frame.grid(row=2,column=1)

        txt = 'Use the correct line\'s URL, otherwise you will get the wrong output!\nA cleaned log speed data table will be created wherever you specified the save location\n\nProgram by abdulwasay12@live.com'

        self.label = tk.Label(parent,text=txt)
        self.label.grid(row=0,column=1)

        #btns frame as 2,1
        b_malts = tk.Button(self.btns_frame, text='Extract Maltesers\' log speed', command = self.maltsExtractor)
        b_malts.grid(row=2, column=1,padx =10)
        b_4line = tk.Button(self.btns_frame, text='Extract 4Line\'s log speed',padx=10, command = self.fourLineExtractor)
        b_4line.grid(row=2, column=2)

        b_cancel = tk.Button(parent, text = 'Quit', command =self.parent.destroy)
        b_cancel.grid(row=3, column=1, pady=10)

    def maltsExtractor(self):

        self.valUrl = self.e.get()

        #url check
        if not re.search("^https?:\/\/",self.valUrl):
            msg.showerror(message='Check URL again! Hint: must start with http',title='Invalid URL')
            self.e.delete(0,tk.END)

        self.dataF = pd.read_html(self.valUrl)
        self.dataF = self.dataF[-1] #get last html table

        new_header = self.dataF.iloc[0]
        self.dataF = self.dataF[1:] #headerless data
        self.dataF.columns = new_header

        # self.dataF.to_csv(f_pth,index=False,sep=',')
        self.dataF.to_clipboard(index=False,header=False)
        msg.showinfo(title='Maltesers',message='Maltesers log speed output copied to clipboard.')

    def fourLineExtractor(self):
        self.valUrl = self.e.get()

        if not re.search("^https?:\/\/",self.valUrl):
            msg.showerror(message='Check URL again! Hint: must start with http',title='Invalid URL')
            self.e.delete(0,tk.END)

        Fourline_html = urlopen(self.valUrl)
        soup = bs(Fourline_html)

        tableCells = soup.find_all('tr',attrs={'class':['TableCell1','TableCell2']})

        dirtyData = []

        for tr in tableCells:
            tds = tr.find_all('td')
            for td in tds:
                dirtyData.append(td.text)

        cleanData = [dirtyData[x:x+13] for x in range(0,len(dirtyData),13)]

        d = pd.DataFrame(cleanData)
        df = pd.DataFrame(cleanData,columns =['Date','Start','Stop','Minutes','Actual Speed','Description','Steel Band','Flap Open','Bullnose Open','Product Sensor','x1','x2','x3'])
        self.finalized_table = df.loc[:,'Date':'Product Sensor']
    
        # self.dataF.to_csv(f_pth,index=False,sep=',')
        self.finalized_table.to_clipboard(index=False,header=False)
        msg.showinfo(title='4Line',message='4Line log speed output copied to clipboard.')

    

window = myClass(tk.Tk())
window.mainloop()
