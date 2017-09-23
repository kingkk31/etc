import os
import _modEXIF
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import logging
import time

#GPS extractor class
class GPSExtractor :

    targetFile = "" #target image file
    info = "" #result string
    lat = None #latitude
    lon = None #longitude

    def __init__(self, root):
        self.root = root
        self.root.geometry("510x500")

        self.frame = Frame(root)
        self.frame.pack()

        #choose image file
        Label(self.frame, text="ImageFile").grid(row=0, pady=5)
        self.e1 = Entry(self.frame, width=40)
        self.e1.grid(row=0, column=1)
        self.btn1 = Button(self.frame, text="search", command=self.seachFile)
        self.btn1.grid(row=0, column=2, pady=10)

        #output Text of result
        self.result = Text(self.frame, wrap=NONE, height=20, width=65)
        self.yS = Scrollbar(self.frame, command=self.result.yview)
        self.xS = Scrollbar(self.frame, orient=HORIZONTAL, command=self.result.xview)
        self.result.config(yscrollcommand=self.yS.set, xscrollcommand=self.xS.set)

        self.result.grid(row=1, column=0, columnspan=3 )
        self.yS.grid(row=1, column=3, sticky='ns')
        self.xS.grid(row=2, column=0, columnspan=3, sticky='ew')

        self.frame2 = Frame(root)
        self.frame2.pack()

        #extracting image
        self.btn2 = Button(self.frame2, text="Extract", command=self.extract)
        self.btn2.grid(row=0, column=1, pady=10)

        #latitude and longitude
        Label(self.frame2, text="latitude").grid(row=1, padx=10, pady=10)
        self.e2 = Entry(self.frame2, width=30)
        self.e2.grid(row=1, column=1)
        Label(self.frame2, text="longitude").grid(row=2, pady=5)
        self.e3 = Entry(self.frame2, width=30)
        self.e3.grid(row=2, column=1)

        #open google maps
        self.btn3 = Button(self.frame2, text="Open map", command=self.openMap)
        self.btn3.grid(row=3, column=1, pady=10)

        mainloop()


    #choose image file
    def seachFile(self):
        name = str(askopenfilename())
        if not name :
            return
        self.e1.delete(0, END)
        self.e1.insert(0, name)


    #extract GPS information
    def extract(self):

        startTime = time.time()

        #log file
        logging.basicConfig(filename='GPSExtractLog.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
        GPSEXTRACTOR_VERSION = "1.0"

        logging.info('+---------------------------------------------+')
        logging.info("GPSExtractor version" + GPSEXTRACTOR_VERSION + " started")

        #get value of entry
        self.targetFile = self.e1.get()

        if self.targetFile == "" :
            tkMessageBox.showerror("No image file", "No image file, Can't extract")
            return

        if os.path.isfile(self.targetFile) :

            #extract GPS information and other information
            gpsDictionary, exifList = _modEXIF.ExtractGPSDictionary(self.targetFile)

            if (gpsDictionary != None):

                #append result
                self.info = ""
                self.info += "+-----------------------------------------------------------" + "\n"
                self.info += "GPS information\n\n"

                for i in gpsDictionary:
                    self.info += str(i) + " : " + str(gpsDictionary[i]) + "\n"
                self.info += "\n"

                self.info += "+-----------------------------------------------------------" + "\n"
                self.info += "Image information\n\n"

                for i in exifList:
                    self.info += str(i) + "\n"
                self.info += "\n"

                #extract latitude, longitude
                dCoor = _modEXIF.ExtractLatLon(gpsDictionary)

                self.info += "+-----------------------------------------------------------" + "\n"
                self.info += "Coordinate\n\n"

                #set entry of latitude, longitude
                if dCoor:
                    for i in dCoor:
                        self.info += str(i) + " : " + str(dCoor[i]) + "\n"
                    self.info += "\n"

                    self.lat = dCoor.get("Lat")
                    latRef = dCoor.get("LatRef")
                    self.lon = dCoor.get("Lon")
                    lonRef = dCoor.get("LonRef")

                    logging.info('latitude : ' + str(self.lat))
                    logging.info('longitude : ' + str(self.lon))

        self.result.delete(1.0, END)
        self.result.insert(END, self.info + "\n")

        self.e2.delete(0, END)
        self.e2.insert(0, str(self.lat))
        self.e3.delete(0, END)
        self.e3.insert(0, str(self.lon))

        endTime = time.time()
        duration = endTime - startTime

        logging.info('Elapsed Time: ' + str(duration) + ' seconds')
        logging.info('Program Terminated Normally')
        logging.info('+---------------------------------------------+')


    #open google maps
    def openMap(self) :

        if self.lat == None or self.lon == None :
            tkMessageBox.showerror("No result", "No result, Can't open map")
            return

        place = str(self.lat) + ',' + str(self.lon)
        url = "https://www.google.co.kr/maps/place/" + place
        os.system("python -m webbrowser -t " + url)