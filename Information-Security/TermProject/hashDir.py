import logging
import time
import _hashDir
from Tkinter import *
from tkFileDialog import *
import ttk
import tkMessageBox

#Directory Hashing Class
class HashDir :
    
    resultHash = [] #result list
    inputDir = "" #target directory
    modeStr = "" #hash mode

    def __init__(self, root):
        self.root = root
        self.root.geometry("510x460")

        self.frame = Frame(root)
        self.frame.pack()

        #open directory
        Label(self.frame, text = "directory").grid(row = 0, pady=5)
        self.e1 = Entry(self.frame, width=40)
        self.e1.grid(row=0, column=1)
        self.btn1 = Button(self.frame, text="search", command=self.seachDir)
        self.btn1.grid(row=0, column=2)

        #choose hash mode
        Label(self.frame, text = "hash mode").grid(row = 1)
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.frame, textvariable=self.box_value, state='readonly', width=37)
        self.box['values'] = ('MD5','SHA1','SHA256','SHA384','SHA512')
        self.box.current(0)
        self.box.grid(row=1, column=1, pady=5)

        #Output Text of result
        self.result = Text(self.frame, wrap=NONE, height=25, width=60)
        self.yS = Scrollbar(self.frame, command=self.result.yview)
        self.xS = Scrollbar(self.frame, orient=HORIZONTAL, command=self.result.xview)
        self.result.config(yscrollcommand=self.yS.set, xscrollcommand=self.xS.set)

        self.result.grid(row=2,column=0, columnspan=3,)
        self.yS.grid(row=2,column=3, sticky='ns')
        self.xS.grid(row=3, column=0, columnspan=3, sticky='ew')

        self.frame2 = Frame(root)
        self.frame2.pack()

        #hashing button
        self.btn2 = Button(self.frame2, text="hashing", command=self.hashing)
        self.btn2.grid(row=0, column=1, pady=8, padx=20)

        #save result into CSV file
        self.btn3 = Button(self.frame2, text="save CSV", command=self.saveCSV)
        self.btn3.grid(row=0, column=2)

        self.resultHash = []

        mainloop()


    #open target directory
    def seachDir(self) :
        name = str(askdirectory())
        if not name :
            return
        self.e1.delete(0, END)
        self.e1.insert(0, name)


    #directory hashing
    def hashing(self) :
        #get value of entry
        self.inputDir = self.e1.get()
        self.modeStr = self.box.get()
        if self.inputDir == "" :
            tkMessageBox.showerror("No directory", "No directory, Can't hashing")
            return

        #log file
        VERSION = '1.0'
        logging.basicConfig(filename='hashDirLog.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

        #set target directory & hash mode
        _hashDir.ParseCommandLine(self.inputDir, self.modeStr)

        startTime = time.time()

        logging.info('')
        logging.info('Welcome to hashDir Version ' + VERSION + ' New Scan Started')
        logging.info('')

        logging.info('System: ' + sys.platform)
        logging.info('Version: ' + sys.version)

        #store result of hasing
        walkPath = _hashDir.WalkPath()
        filesProcessed = walkPath[0]
        self.resultHash = walkPath[1]

        #Output of result
        self.result.delete(1.0, END)
        element = ['File', 'Path', 'Size', 'Modified Time', 'Access Time', 'Created Time', 'hashType', 'hashValue', 'Owner', 'Group', 'Mode']
        for i in range(len(self.resultHash)) :
            self.result.insert(END, "+-----------------------------------------------------------" + "\n\n")
            for j in range(len(self.resultHash[i])) :
                self.result.insert(END, str(element[j]) +  ":" + str(self.resultHash[i][j]) + "\n\n")
        self.result.insert(END, "+-----------------------------------------------------------" + "\n\n")

        endTime = time.time()
        duration = endTime - startTime

        logging.info('Files Processed: ' + str(filesProcessed))
        logging.info('Elapsed Time: ' + str(duration) + ' seconds')
        logging.info('')
        logging.info('Program Terminated Normally')
        logging.info('')


    #save result into CSV file
    def saveCSV(self) :
        if self.resultHash == [] :
            tkMessageBox.showerror("No result", "No result, Can't save CSV")
            return

        #choose path of CSV file
        filePath = askdirectory()
        dirName =  '/' + str(self.inputDir).split('/')[-1]

        #create CSV file
        oCVS = _hashDir._CSVWriter(filePath + dirName + 'fileSystemReport.csv', self.modeStr)

        #write row of result
        for i in self.resultHash:
            oCVS.writeCSVRow(i[0], i[1], i[2], i[3], i[4], i[5], i[7], i[8], i[9], i[10])
        oCVS.writerClose()
        tkMessageBox.showinfo("Save", "Save")

