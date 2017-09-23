from Tkinter import *
import hashDir
import searchKeyword
import GPSExtractor
import portScanner

#Directory Hashing window open
def dirHash() :
    newWindow = Toplevel(root)
    app = hashDir.HashDir(newWindow)

#Searching Keyword window open
def searchKey() :
    newWindow = Toplevel(root)
    app = searchKeyword.SearchKeyword(newWindow)

#Extracting GPS window open
def GPSExtract() :
    newWindow = Toplevel(root)
    app = GPSExtractor.GPSExtractor(newWindow)

#Scanning port window open
def scanOpenPort() :
    newWindow = Toplevel(root)
    app = portScanner.ScanPort(newWindow)


root = Tk()
root.geometry("200x190")
frame = Frame(root)
frame.pack()

#Buttons are open new window

btn1 = Button(frame, text="Directory Hashing", command=dirHash)
btn1.grid(row=0, pady=10)

btn2 = Button(frame, text="Searching Keywords", command=searchKey)
btn2.grid(row=1, pady=10)

btn3 = Button(frame, text="Extracting GPS of Picture", command=GPSExtract)
btn3.grid(row=2, pady=10)

btn4 = Button(frame, text="Scanning Open Port", command=scanOpenPort)
btn4.grid(row=3, pady=10)

mainloop()