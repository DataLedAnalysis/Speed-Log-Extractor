import tkinter as tk
import pandas as pd
from tkinter import messagebox as msg, filedialog as fd
from datetime import date

#/home/abdul/Documents/Python/Speed-Log-Extractor/table.html


class myClass(tk.Frame):       
    def __init__(self,parent):
        super().__init__(parent)
        #create an entry widget
        self.e = tk.Entry(parent) #using self.master produces text
        self.e.grid(row=1,column=1)

        b = tk.Button(parent, text='Submit', command = self.tableExtractor1)
        b.grid(row=3, column=1)

    def close(self):
        return 
    
    def tableExtractor1(self):
        self.valUrl = self.e.get()
        self.dataF = pd.read_html(self.valUrl)
        self.dataF = self.dataF[0]


        d = date.today().strftime('%d%b%y')
        fname = d + '_Maltesers'
        f_pth = fd.asksaveasfile(initialfile= fname, defaultextension='.csv'
                                 ,filetypes=[('Comma Delimited Files',"*.csv")])
        self.dataF.to_csv(f_pth,sep=';')
        self.master.destroy()

window = myClass(tk.Tk())
window.mainloop()

"""



"""

