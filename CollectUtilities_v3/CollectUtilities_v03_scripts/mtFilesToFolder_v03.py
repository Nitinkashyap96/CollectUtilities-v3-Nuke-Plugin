#============================================
# V1.0
# MIGUEL TORIJA
# 30/11/2002
#============================================
#
#mtFiles_To_Folder
#
#============================================





import shutil, os, nuke, nukescripts, threading, time, datetime
import webbrowser



from PySide2 import QtWidgets, QtCore, QtUiTools



class mtFilesToFolder:

    def __init__(self, ui):

        #path_ui = "C:/Users/Usuario/.nuke/CollectUtilities_v3/ui/mtFilesToFolder_v001.ui"
        path_ui = ui
        try:
            toFillReadsLIST = []
            toFillDeepReadsLIST = []
            toFillReads = nuke.selectedNodes('Read')
            toFillDeepReads = nuke.selectedNodes('DeepRead')
            toFillReadsG = nuke.selectedNodes('ReadGeo2')
            for i in toFillReads:
                nrc = i.knob('name').value()
                toFillReadsLIST.append(nrc)

            for i in toFillDeepReads:
                nrc = i.knob('name').value()
                toFillDeepReadsLIST.append(nrc)

            for i in toFillReadsG:
                nrc = i.knob('name').value()
                toFillReadsLIST.append(nrc)

            toFillReadsLIST.extend(toFillDeepReadsLIST)
            str_1 = ", "
            toFillReadsString = str_1.join(toFillReadsLIST)
        except:
            raise
            toFillReadsString = ""


        self.wgFolder = QtUiTools.QUiLoader().load(path_ui)

        # SETUP ---------------

        self.wgFolder.lineEditReadsToCopy.setText(toFillReadsString)

        # MAIN SIGNALS ---------------

        self.wgFolder.btnPath.clicked.connect(self.press_btnPath)        
        self.wgFolder.btnToFolder.clicked.connect(self.press_btnToFolder)


        # Other Signals
        self.wgFolder.btnWEB.clicked.connect(self.press_btnWEB)
        self.wgFolder.btnInfo.clicked.connect(self.press_btnInfo)


        # RUN ---------------
        self.wgFolder.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.wgFolder.show()


    def press_btnInfo(self):
        webbrowser.open("https://www.migueltorija.com/post/user-guide-mtcollect-utilities-v3-0")

    def press_btnWEB(self):
        webbrowser.open("https://www.migueltorija.com/")

    def press_btnPath(self):

        self.wgFolder.hide()

        PathToSave = nuke.getFilename('Select a Folder')

        self.wgFolder.show()

        self.wgFolder.lblPath.setText(PathToSave)



    def press_btnToFolder(self):

        openFolder = self.wgFolder.cbContainerFolder.isChecked()

        self.wgFolder.hide()
        def set_Progress_Bar(barprog):
            progress_BAR = nuke.ProgressTask("Copying Footage")
            bar = barprog
            tasks = 2
            percent = int(100*(float(bar) / (tasks+1)))
            progress_BAR.setProgress(percent)
            progress_BAR.setMessage("Step {} of {}".format(bar, tasks))
            time.sleep(0.1)
            if bar == 2:
                del(progress_BAR)
            else:
                pass
        set_Progress_Bar(1)      
        myProjectRoot = nuke.root().knob('name').value()

        myProject = os.path.basename(myProjectRoot)
        myRoot = os.path.dirname(myProjectRoot)
        myProjectcut = myProject[0:-3]

        listToCopyInFolder = []
        listToCopyInFolder2 = []
        listToCopyInFolderG = []
        listToCopyInFolderG2 = []

        for i in nuke.selectedNodes('Read'):
            readsCopy = i.knob('name').value()
            listToCopyInFolder.append(readsCopy)

        for i in nuke.selectedNodes('DeepRead'):
            readsCopy = i.knob('name').value()
            listToCopyInFolder.append(readsCopy)

        for n in nuke.allNodes('Read'):
            readsCopy2 = n.knob('name').value()
            listToCopyInFolder2.append(readsCopy2)

        for i in nuke.selectedNodes('ReadGeo2'):
            readsCopyG = i.knob('name').value()
            listToCopyInFolderG.append(readsCopyG) 

        for i in nuke.allNodes('ReadGeo2'):
            readsCopyG2 = i.knob('name').value()
            listToCopyInFolderG2.append(readsCopyG2)    


        str1 = ", "

        readsString = str1.join(listToCopyInFolder)
        readsStringCheck = str1.join(listToCopyInFolder2)
        readsStringG = str1.join(listToCopyInFolderG)
        readsStringG2 = str1.join(listToCopyInFolderG2)


        if len(listToCopyInFolderG) > 0:
            ReadsToCopy_INPUT = readsString+ ", " + readsStringG
        else:
            ReadsToCopy_INPUT = readsString


        destination = self.wgFolder.lblPath.text()
        openThisFolder = self.wgFolder.lblPath.text()
        copiedNodes = []
        copiedFilepaths = []


        ReadsToCopy = self.wgFolder.lineEditReadsToCopy.text()
        ReadsToCopylist = ReadsToCopy.split(", ")


        lenReadsCopyList = len(ReadsToCopylist)


        for i in ReadsToCopylist:

            if lenReadsCopyList == 0:
                break
            else:
                pass

            name = i
            targetN = nuke.toNode(i)
            readFile = targetN.knob('file').value()




            if readFile == "":
                continue
            else:
                pass

            if os.path.isabs(readFile) == False:
                
                readFile = myRoot + "/" + readFile
            else:
                
                pass
            print (readFile)

            readFilePath = os.path.dirname(readFile)
            readBaseName = os.path.basename(readFile)
            nameExtension = os.path.splitext(readBaseName)
            filename = nameExtension[0]
            fileExtension = nameExtension[1]


            
            seqList = [".exr", ".dpx", ".jpg", ".png", ".tiff", ".targa", ".jpeg" ]

            if readFile in copiedFilepaths:
                continue
            else:
                pass

            if name in copiedNodes:
                continue
            else:
                pass

            if name not in ReadsToCopylist:
                continue
            else:
                pass


            if targetN.Class() == 'Read' or targetN.Class() == 'DeepRead':


                if filename.find(str("%d")) != -1 or filename.find(str("%02d")) != -1 or  filename.find(str("%03d")) != -1 or  filename.find(str("%04d")) != -1 or filename.find(str("%05d")) != -1 or filename.find(str("%06d")) != -1 or filename.find(str("%07d")) != -1 or filename.find(str("%08d")) != -1 or filename.find(str("####")) != -1:
                    if fileExtension in seqList:
                        print ("image sequence")

                        readFirst = targetN['first'].value()
                        readLast = targetN['last'].value()

                        for e in range(readFirst, readLast+1):
                            
                            if filename.find(str("%04d")) != -1:
                                try:
                                    if len (str(e))<4:
                                        badLen = len(str(e))
                                        difLen = 4 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass

                                    readBaseNameFraming = readBaseName.replace("%04d", str(fixNum))
                                except:
                                    pass

                            elif filename.find(str("%d")) != -1:
                                try:
                                    if len (str(e))<1:
                                        badLen = len(str(e))
                                        difLen = 1 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass
                                    readBaseNameFraming = readBaseName.replace("%d", str(fixNum))
                                except:
                                    pass
                            elif filename.find(str("%03d")) != -1:
                                try:
                                    if len (str(e))<3:
                                        badLen = len(str(e))
                                        difLen = 3 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass
                                    readBaseNameFraming = readBaseName.replace("%03d", str(fixNum))
                                except:
                                    pass
                            elif filename.find(str("%02d")) != -1:
                                try:
                                    if len (str(e))<2:
                                        badLen = len(str(e))
                                        difLen = 2 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass
                                    readBaseNameFraming = readBaseName.replace("%02d", str(fixNum))
                                except:
                                    pass
                            elif filename.find(str("%05d")) != -1:
                                try:
                                    if len (str(e))<5:
                                        badLen = len(str(e))
                                        difLen = 5 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass
                                    readBaseNameFraming = readBaseName.replace("%05d", str(fixNum))
                                except:
                                    pass
                            elif filename.find(str("%06d")) != -1:
                                try:
                                    if len (str(e))<6:
                                        badLen = len(str(e))
                                        difLen = 6 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass
                                    readBaseNameFraming = readBaseName.replace("%06d", str(fixNum))
                                except:
                                    pass
                            elif filename.find(str("%07d")) != -1:
                                try:
                                    if len (str(e))<7:
                                        badLen = len(str(e))
                                        difLen = 7 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass
                                    readBaseNameFraming = readBaseName.replace("%07d", str(fixNum))
                                except:
                                    pass
                            elif filename.find(str("%08d")) != -1:
                                try:
                                    if len (str(e))<8:
                                        badLen = len(str(e))
                                        difLen = 8 - badLen
                                        multLen = '0'*difLen
                                        fixNum = multLen+str(e)
                                    else:
                                        fixNum = e
                                        pass
                                    readBaseNameFraming = readBaseName.replace("%08d", str(fixNum))
                                except:
                                    pass
                            elif filename.find(str("####")) != -1:
                                try:
                                    readBaseNameFraming = readBaseName.replace("####", str(e))
                                except:
                                    pass
                            else:
                                pass

                            #print readBaseNameFraming

                            fileToCopy = str(readFilePath) +"/"+ str(readBaseNameFraming)
                            print (fileToCopy)

                            try:
                                if e == readFirst:
                                    
                                    if filename.find(str("%04d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%04d", "")
                                        except:
                                            pass
                                    elif filename.find(str("%d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%d", "")
                                        except:
                                            pass
                                    elif filename.find(str("%2d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%2d", "")
                                        except:
                                            pass
                                    elif filename.find(str("%3d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%3d", "")
                                        except:
                                            pass
                                    elif filename.find(str("%05d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%05d", "")
                                        except:
                                            pass
                                    elif filename.find(str("%06d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%06d", "")
                                        except:
                                            pass
                                    elif filename.find(str("%07d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%07d", "")
                                        except:
                                            pass
                                    elif filename.find(str("%08d")) != -1:
                                        try:
                                            filenameFix = filename.replace("%08d", "")
                                        except:
                                            pass
                                    elif filename.find(str("####")) != -1:
                                        try:
                                            filenameFix = filename.replace("####", "")
                                        except:
                                            pass
                                    else:
                                        filenameFix = filename


                                    os.makedirs(destination+str(filenameFix))
                                    folderToPlaceCopy = destination+str(filenameFix)                                
                                    shutil.copy(str(fileToCopy), str(folderToPlaceCopy))


                                elif e == readLast:
                                    shutil.copy(str(fileToCopy), str(folderToPlaceCopy))
                                    copiedNodes.append(name)
                                    copiedFilepaths.append(readFile)

                                else:
                                    shutil.copy(str(fileToCopy), str(folderToPlaceCopy))
                                continue
                            except:
                                print ("something happened trying to copy a image sequence")
                                raise
                                continue
                else:
                    print ("movie")
                    
                    try:
                        os.makedirs(destination+str(filename))
                        folderToPlaceCopy = destination+str(filename)
                        
                        shutil.copy(str(readFile), str(folderToPlaceCopy))
                        copiedNodes.append(name)
                        copiedFilepaths.append(readFile)

                    except:
                        print ("something happened trying to copy a movie")
                        continue

            elif targetN.Class() == 'ReadGeo2':
                try:
                    os.makedirs(destination+str(filename))
                    folderToPlaceCopy = destination+str(filename)
                    
                    shutil.copy(str(readFile), str(folderToPlaceCopy))
                    copiedNodes.append(name)
                    copiedFilepaths.append(readFile)

                except:
                    continue

            else:
                pass


        set_Progress_Bar(2) 
        self.wgFolder.close()
        j = nuke.message('All Files copied!')
        print (openFolder)
        if openFolder == True:
            print (openThisFolder)
            openThisFolderNormalize = openThisFolder.replace('/', '\\')
            os.system('explorer %s' % openThisFolderNormalize)

        else:
            pass

def load_mtFilesToFolder(ui_load):
    global tool 
    ui = ui_load
    tool = mtFilesToFolder(ui)