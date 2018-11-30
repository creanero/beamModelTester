# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 14:43:43 2018

@author: User
"""

import Tkinter


class Values(Tkinter.Tk):
    """docstring for Values"""
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        stepOne = Tkinter.LabelFrame(self, text=" 1. Enter Values ")
        stepOne.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.Val1Lbl = Tkinter.Label(stepOne,text="Value 1")
        self.Val1Lbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.Val1Txt = Tkinter.Entry(stepOne)
        self.Val1Txt.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val2Lbl = Tkinter.Label(stepOne,text="Value 2")
        self.Val2Lbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.Val2Txt = Tkinter.Entry(stepOne)
        self.Val2Txt.grid(row=1, column=1, columnspan=3, pady=2, sticky='WE')

        self.val1 = None
        self.val2 = None

        SubmitBtn = Tkinter.Button(stepOne, text="Submit",command=self.submit)
        SubmitBtn.grid(row=4, column=3, sticky='W', padx=5, pady=2)

    def submit(self):
        self.val1=self.Val1Txt.get()
        if self.val1=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.val2=self.Val2Txt.get()
        if self.val2=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.quit()


if __name__ == '__main__':
    app = Values(None)
    app.title('Values')
    app.mainloop() #this will run until it closes
    #Print the stuff you want.
    print app.val1,app.val2