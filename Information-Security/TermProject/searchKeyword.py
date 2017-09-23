import logging
import time
import _searchKeyword
from Tkinter import *
from tkFileDialog import *
import tkMessageBox

#Searching Keyword Class
class SearchKeyword :

    inputFile = "" #target file
    keyFile = "" #keyword file
    resultStr = NONE #result string

    def __init__(self, root):
        self.root = root
        self.root.geometry("660x475")

        self.frame = Frame(self.root)
        self.frame.pack()

        #choose target file
        Label(self.frame, text = "Target File").grid(row = 0)
        self.e1 = Entry(self.frame, width=45)
        self.e1.grid(row=0, column=1)
        self.btn1 = Button(self.frame, text="search", command=self.search1)
        self.btn1.grid(row=0, column=2, pady=3)

        #choose keyword file
        Label(self.frame, text="Keyword File").grid(row = 1)
        self.e2 = Entry(self.frame, width=45)
        self.e2.grid(row=1, column=1)
        self.btn2 = Button(self.frame, text="search", command=self.search2)
        self.btn2.grid(row=1, column=2, pady=5)

        #Output Text of result
        self.result = Text(self.frame, wrap=NONE, height=25, width=80)
        self.yS = Scrollbar(self.frame, command=self.result.yview)
        self.xS = Scrollbar(self.frame, orient=HORIZONTAL, command=self.result.xview)
        self.result.config(yscrollcommand=self.yS.set, xscrollcommand=self.xS.set)

        self.result.grid(row=2, column=0, columnspan=3, sticky='nsew')
        self.yS.grid(row=2, column=3, sticky='ns')
        self.xS.grid(row=3, column=0, columnspan=3, sticky='ew')

        self.frame2 = Frame(root)
        self.frame2.pack()

        #searching button
        self.btn3 = Button(self.frame2, text="Search Keywords", command=self.searchingKeywords)
        self.btn3.grid(row=0, column=1, pady=14, padx=20)

        #save result into txt file
        self.btn4 = Button(self.frame2, text="Save txt", command=self.saveTXT)
        self.btn4.grid(row=0, column=2)

        self.resultStr = None

        mainloop()


    #choose target file
    def search1(self) :
        name = str(askopenfilename())
        if not name:
            return
        self.e1.delete(0, END)
        self.e1.insert(0, name)


    #choose keyword file
    def search2(self) :
        name = str(askopenfilename())
        if not name:
            return
        self.e2.delete(0, END)
        self.e2.insert(0, name)


    #searching keywords
    def searchingKeywords(self) :

        # get value of entry
        self.inputFile = self.e1.get()
        self.keyFile = self.e2.get()

        if self.inputFile == "" or self.keyFile == "" :
            tkMessageBox.showerror("No file", "No file, Can't searching")
            return

        SEARCHKEYWORD_VERSION = '1.0'

        #log file
        logging.basicConfig(filename='searchKeywordLog.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

        # set target & keyword file
        _searchKeyword.ParseCommandLine(self.inputFile, self.keyFile)

        log = logging.getLogger('main._searchKeyword')
        log.info("searchKeyword version" + SEARCHKEYWORD_VERSION + " started")

        startTime = time.time()

        #search keyword
        self.resultStr = _searchKeyword.SearchWords()

        #output of result
        self.result.delete(1.0, END)
        self.result.insert(END, self.resultStr)

        endTime = time.time()
        duration = endTime - startTime

        logging.info('Elapsed Time: ' + str(duration) + ' seconds')
        logging.info('')
        logging.info('Program Terminated Normally')


    #save result into txt file
    def saveTXT(self) :

        if self.resultStr == None :
            tkMessageBox.showerror("No result", "No result, Can't save TXT")
            return

        #choose path of txt file
        filePath = askdirectory()
        fileName =  ('/' + str(self.inputFile).split('/')[-1]).split('.')[0]

        #create txt file
        saveFile = open(filePath + fileName + "searchingReport.txt", 'w')
        saveFile.write(self.resultStr)
        saveFile.close()

        tkMessageBox.showinfo("Save", "Save")