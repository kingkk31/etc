from Tkinter import *
import tkMessageBox
from datetime import datetime
import struct
from socket import *
import socket
import logging
from tkFileDialog import *
import csv

#port scanner class
class ScanPort :

    startAddress = "" #start IP address
    endAddress = "" #end IP address
    startPort = None #start port
    endPort = None #start port

    def __init__(self, root):

        self.resultList = []

        self.root = root
        self.root.geometry("660x485")

        self.frame = Frame(self.root)
        self.frame.pack()

        #start IP address
        Label(self.frame, text = "Start Address").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.e1 = Entry(self.frame, width=20)
        self.e1.grid(row=0, column=1, padx=5, pady=5)

        #end IP address
        Label(self.frame, text="End Address").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.e2 = Entry(self.frame, width=20)
        self.e2.grid(row=0, column=3, padx=5, pady=5)

        #start port
        Label(self.frame, text="Start Port").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.e3 = Entry(self.frame, width=20)
        self.e3.grid(row=1, column=1, padx=5, pady=5)

        #end port
        Label(self.frame, text="End Port").grid(row=1, column=2, padx=5, pady=5, sticky=W)
        self.e4 = Entry(self.frame, width=20)
        self.e4.grid(row=1, column=3, padx=5, pady=5)

        #scan
        self.btn1 = Button(self.frame, text="Scan", command=self.scan)
        self.btn1.grid(row=2, column=1, pady=15)

        #save CSV file
        self.btn2 = Button(self.frame, text="Save CSV", command=self.saveCSV)
        self.btn2.grid(row=2, column=2, pady=15)

        self.frame2 = Frame(self.root)
        self.frame2.pack()

        #Output Text of result
        self.result = Text(self.frame2, wrap=NONE, height=25, width=60, fg="white", bg="midnight blue")
        self.yS = Scrollbar(self.frame2, command=self.result.yview)
        self.xS = Scrollbar(self.frame2, orient=HORIZONTAL, command=self.result.xview)
        self.result.config(yscrollcommand=self.yS.set, xscrollcommand=self.xS.set)

        self.result.grid(row=0,column=0)
        self.yS.grid(row=0,column=1, sticky='ns')
        self.xS.grid(row=1, column=0,sticky='ew')

        mainloop()


    #scan
    def scan(self):

        if(self.e1.get() == "" or self.e2.get() == "" or self.e3.get() == "" or self.e4.get() == "") :
            tkMessageBox.showerror("No input", "No input, Can't scan")
            return

        self.result.delete(1.0, END)

        #get value of entry
        self.startAddress = self.e1.get()
        self.endAddress = self.e2.get()
        self.startPort = int(self.e3.get())
        self.endPort = int(self.e4.get())

        #scan start
        self.scanStart(self.startAddress, self.endAddress, self.startPort, self.endPort)


    #save CSV file
    def saveCSV(self):

        if self.resultList == [] :
            tkMessageBox.showerror("No result", "No result, Can't save CSV")
            return

        try:
            #choose path of CSV file
            filePath = askdirectory()
            csvFile = open(filePath+ '/ScanPortReport.csv', 'wb')
            writer = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_ALL)

            #write result
            writer.writerow(('ipAddress', 'port'))
            for i in self.resultList :
                for j in i[1] :
                    writer.writerow((i[0], j))
            csvFile.close()
        except:
            logging.error('CSV File Failure')

        tkMessageBox.showinfo("Save", "Save")


    #split IP address range
    def getIpAddressesFromRange(self, startAddress, endAddress):
        ipstruct = struct.Struct('>I')
        start, = ipstruct.unpack(inet_aton(startAddress))
        end, = ipstruct.unpack(inet_aton(endAddress))
        return [inet_ntoa(ipstruct.pack(i)) for i in range(start, end + 1)]


    #port scan
    def portScanIPAddress(self, ipAdd, startPort, endPort):

        remoteServer = ipAdd
        remoteServerIP = socket.gethostbyname(remoteServer)

        self.result.insert(END, ("-" * 60) + "\n")
        self.result.insert(END, "Scanning remote host " + str(remoteServer) + "\n")
        self.result.insert(END, ("-" * 60) + "\n")

        portOpenCount = 0
        portList = []

        t1 = datetime.now()

        #create socket and connect
        try:
            for port in range(startPort, endPort + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((remoteServerIP, port))

                # connected
                if result == 0:
                    #append result
                    self.result.insert(END, "Port " + str(port) + " Open" + "\n")
                    portList.append(str(port))
                    portOpenCount += 1
                sock.close()
            logging.info('Open Port Found: ' + str(portOpenCount))

        except KeyboardInterrupt:
            self.result.insert(END, "You pressed Ctrl+C" + "\n")
            sys.exit()

        except socket.gaierror:
            self.result.insert(END, "Hostname could not be resolved. Exiting" + "\n")
            sys.exit()

        except socket.error:
            self.result.insert(END, "Couldn't connect to server" + "\n")
            sys.exit()

        t2 = datetime.now()

        total = t2 - t1

        self.result.insert(END, "\nScanning Completed in: " + str(total) + "\n")

        return portList


    #scan start
    def scanStart(self, startAddress, endAddress, starPort, endPort):

        #result list
        self.resultList = []

        PORTSCAN_VERSION = '1.0'

        #log file
        logging.basicConfig(filename='portScanLog.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

        log = logging.getLogger('main.port')
        log.info("portScan version" + PORTSCAN_VERSION + " started")

        #get IP address range
        ipRange = self.getIpAddressesFromRange(startAddress, endAddress)

        #scan and get result
        for addr in ipRange:
            logging.info('Port Scan on IP Address: ' + addr)
            portList = self.portScanIPAddress(addr, starPort, endPort)
            self.resultList.append((str(addr), portList))
