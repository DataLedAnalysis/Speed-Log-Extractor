import tkinter as tk
import pandas as pd
from tkinter import messagebox as msg, filedialog as fd
from datetime import date

#/home/abdul/Documents/Python/Speed-Log-Extractor/table.html


class myClass(tk.Frame):       
    def __init__(self,parent):
        super().__init__(parent)
        #create an entry widget
        self.parent = parent
        self.parent.title('Hello')
        
        self.e = tk.Entry(parent) #using self.master produces text
        self.e.grid(row=1, column=1)

        b = tk.Button(parent, text='Maltesers', command = self.tableExtractor1)
        b_cancel = tk.Button(parent, text = 'Quit', command =self.parent.destroy)

        b.grid(row=3, column=1)
        b_cancel.grid(row=3, column=2)
    
    def tableExtractor1(self):
        self.valUrl = self.e.get()
        self.dataF = pd.read_html(self.valUrl)
        self.dataF = self.dataF[-1] #get last html table
        
        new_header = self.dataF.iloc[0]
        self.dataF = self.dataF[1:] #headerless data
        self.dataF.columns = new_header

        d = date.today().strftime('%d%b%y')
        fname = d + '_Maltesers'
        f_pth = fd.asksaveasfilename(initialfile=fname,defaultextension='xlsx',filetypes=[('Excel','*.xlsx')])
        # self.dataF.to_csv(f_pth,index=False,sep=',')
        self.dataF.to_excel(f_pth, index=False)
        self.master.destroy()

window = myClass(tk.Tk())
window.mainloop()
