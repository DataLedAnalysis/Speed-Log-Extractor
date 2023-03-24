import tkinter as tk, re
import pandas as pd
from tkinter import messagebox as msg, filedialog as fd
from datetime import date
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

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
            self.maltsExtractor
       
        self.dataF = pd.read_html(self.valUrl)
        self.dataF = self.dataF[-1] #get last html table

        new_header = self.dataF.iloc[0]
        self.dataF = self.dataF[1:] #headerless data
        self.dataF.columns = new_header

        d = date.today().strftime('%d%b%y')
        fname = d + '_Maltesers'
        f_pth = fd.asksaveasfilename(initialfile=fname,defaultextension='xlsx',filetypes=[('Excel','*.xlsx')])

        if bool(f_pth) == False: #exit if quit is pressed
            msg.showinfo(title='Quitting',message='You decided to quit this file dialog, exiting the program. \n\nNOTE: You need to re-run, if you want to reuse this program again.')
            sys.exit()
        else:    
        # self.dataF.to_csv(f_pth,index=False,sep=',')
            self.dataF.to_excel(f_pth, index=False)
            self.e.delete(0,tk.END)
            msg.showinfo(title='Maltesers',message='Maltesers log speed output saved. You may quit the program now.')

    def fourLineExtractor(self):
        self.valUrl = self.e.get()

        if not re.search("^https?:\/\/",self.valUrl):
            msg.showerror(message='Check URL again! Hint: must start with http',title='Invalid URL')
            self.e.delete(0,tk.END)
            self.fourLineExtractor
        
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
        finalized_table = df.loc[:,'Date':'Product Sensor']
    
        d = date.today().strftime('%d%b%y')
        fname = d + '_4Line'
        f_pth = fd.asksaveasfilename(initialfile=fname,defaultextension='xlsx',filetypes=[('Excel','*.xlsx')])

        if bool(f_pth) == False: #exit if quit is pressed
            msg.showinfo(title='Quitting',message='You decided to quit this file dialog, exiting the program. \n\nNOTE: You need to re-run, if you want to reuse this program again.')
            sys.exit()
        else:    
        # self.dataF.to_csv(f_pth,index=False,sep=',')
            finalized_table.to_excel(f_pth, index=False)
            self.e.delete(0,tk.END)
            msg.showinfo(title='4Line',message='4Line log speed output saved. You may quit the program now.')

    

window = myClass(tk.Tk())
window.mainloop()
