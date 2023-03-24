import tkinter as tk, re
import pandas as pd
from tkinter import messagebox as msg, filedialog as fd
from datetime import date
import sys

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

        #btns frame as 2,1
        b_malts = tk.Button(self.btns_frame, text='Extract Maltesers\' log speed', command = self.maltsExtractor)
        b_malts.grid(row=2, column=1,padx =10)
        b_4line = tk.Button(self.btns_frame, text='Extract 4Line\'s log speed',padx=10)
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
            msg.showinfo(title='Maltesers',message='Maltesers log speed output saved. You may quit the program now.')

window = myClass(tk.Tk())
window.mainloop()
