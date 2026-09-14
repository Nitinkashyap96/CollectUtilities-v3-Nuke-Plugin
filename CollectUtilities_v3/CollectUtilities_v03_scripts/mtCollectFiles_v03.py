#*********************************************************************
# content   = mtCollectFiles
# date      = 2021-05-12
#
# author    = Miguel Torija <migueltorija.com>
#*********************************************************************


import os
import sys
import threading

import webbrowser

import shutil
import psutil

import time
import datetime

import nuke
import nukescripts

try:
    from PySide2 import QtWidgets, QtCore, QtUiTools
except ImportError:
    from PySide6 import QtWidgets, QtCore, QtUiTools

#*********************************************************************

class mtCollectFiles():

    def __init__(self, ui, ui_advise):

        #path_ui = "C:/Users/Usuario/.nuke/CollectUtilities_v3/ui/mtCollectFiles_v002.ui"
        path_ui = ui

        path_ui_advise = ui_advise

        MY_PROJECT_ROOT = nuke.root().knob('name').value()
        MY_PROJECT_NAME = os.path.basename(MY_PROJECT_ROOT)
        MY_PROJECT_PATH = os.path.dirname(MY_PROJECT_ROOT)
        MY_PROJECT_NAME_CUT = MY_PROJECT_NAME[0:-3]

        PathToSave = MY_PROJECT_PATH
    

        self.wgHeader = QtUiTools.QUiLoader().load(path_ui)

        # SETUP ---------------
        self.wgHeader.lnlDestination.setText(PathToSave)
        self.wgHeader.lineEditFolderName.setText(MY_PROJECT_NAME_CUT + "_collected")
        self.wgHeader.lineEditScriptName.setText("collected_"+MY_PROJECT_NAME)

        # MAIN SIGNALS ---------------
        self.wgHeader.btnSelectFolder.clicked.connect(self.press_btnSelectFolder)

        self.wgHeader.btnCollectFiles.clicked.connect(self.press_btnCollectFiles)

        # Other Signals
        self.wgHeader.btnWEB.clicked.connect(self.press_btnWEB)
        self.wgHeader.btnInfo.clicked.connect(self.press_btnInfo)

        # RUN ---------------
        self.wgHeader.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.wgHeader.show()


        #------------------ ULTIMATUM --------------------

        self.wgADVICE = QtUiTools.QUiLoader().load(path_ui_advise)
        self.wgADVICE.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.wgADVICE.btnYES.clicked.connect(self.press_btnYES)
        self.wgADVICE.btnNO.clicked.connect(self.press_btnNO)

    #*********************************************************************
    # PRESS
    def press_btnInfo(self):
        webbrowser.open("https://www.migueltorija.com/post/user-guide-mtcollect-utilities-v3-0")

    def press_btnWEB(self):
        webbrowser.open("https://www.migueltorija.com/")

    def press_btnSelectFolder(self):

        self.wgHeader.hide()

        PathToSave = nuke.getFilename('Select a Folder')

        self.wgHeader.show()

        self.wgHeader.lnlDestination.setText(PathToSave)

    def press_btnCollectFiles(self):
        self.wgADVICE.show()    

    def press_btnNO(self):
        self.wgADVICE.close()


    def press_btnYES(self):

        #Creating Useful variables about the Project and the main Lists to store the copied Nodes 
        print ('Check 00, The button is working')

        MY_PROJECT_ROOT = nuke.root().knob('name').value()
        MY_PROJECT_NAME = os.path.basename(MY_PROJECT_ROOT)
        MY_PROJECT_PATH = os.path.dirname(MY_PROJECT_ROOT)
        MY_PROJECT_NAME_CUT = MY_PROJECT_NAME[0:-3]

        OLD_DATA = nukescripts.get_script_data()

        copiedNodes = []
        copiedFilepaths = []

        # Checking UI selections
        PathToSave = self.wgHeader.lnlDestination.text()
        FolderNameToSave = self.wgHeader.lineEditFolderName.text()
        ScriptNameToSave = self.wgHeader.lineEditScriptName.text()

        ReadsToExclude = self.wgHeader.lineEditExcludeReads.text()
        GeoToExclude = self.wgHeader.lineEditExcludeGeo.text()

        CopyGeoFiles = self.wgHeader.cbCreateGeoFolder.isChecked()
        RemoveSolitaryReads = self.wgHeader.cbRemoveSolitary.isChecked()
        RemoveNotCopiedReads = self.wgHeader.cbRemoveNotCopiead.isChecked()
        openContainerFolder = self.wgHeader.cbOpenFolder.isChecked()


        print (MY_PROJECT_ROOT)
        print (MY_PROJECT_NAME)
        print (MY_PROJECT_PATH)
        print (PathToSave)
        print (CopyGeoFiles)
        print (RemoveSolitaryReads)
        print (RemoveNotCopiedReads)
        print (FolderNameToSave)
        print (ScriptNameToSave)
        print (ReadsToExclude)
        print (GeoToExclude)



        DESTINATION = PathToSave
        MAINFOLDER = FolderNameToSave
        SCRIPT_NAME = "/"+ScriptNameToSave

        print ('DESTINATION: '+DESTINATION)
        print ('MAINFOLDER: '+MAINFOLDER)
        print ('SCRIPT_NAME: '+SCRIPT_NAME)
        #-------------------------

        nuke.scriptSave("")

        #-------------------------

        print ('Check 01, After gathering info')
        #Creating the main folder and New script activating the relative paths

        collected = os.makedirs(DESTINATION+MAINFOLDER)

        nuke.scriptSaveAs(DESTINATION+MAINFOLDER+SCRIPT_NAME)

        nuke.root().knob('project_directory').setValue("[python {nuke.script_directory()}]")

        #Footage Directory

        os.makedirs(DESTINATION+MAINFOLDER+"/footage")

        print ('Check 02, After making Footage directories')


        # Creating the Progress Bar 

        


        def set_Progress_Bar(barprog):
            progress_BAR = nuke.ProgressTask("Copying Footage")
            bar = barprog
            tasks = 8
            percent = int(100*(float(bar) / (tasks+1)))
            progress_BAR.setProgress(percent)
            progress_BAR.setMessage("Step {} of {}".format(bar, tasks))
            time.sleep(0.1)
            if bar == 8:
                del(progress_BAR)
            else:
                pass
        set_Progress_Bar(1000)

        print ('Check 04, After creating TimeBar')
        #========================================================================
        # REMOVING SOLITARY READS
        #========================================================================

        if RemoveSolitaryReads == True:

            for rem in nuke.allNodes('Read'):

                toCheck = rem.knob('name').value()
                nodeToCheck = nuke.toNode(toCheck)

                a = nodeToCheck.dependent()

                if len(a) == 0:
                    nuke.delete(nodeToCheck)

                else:
                    pass

            for rem in nuke.allNodes('DeepRead'):

                toCheck = rem.knob('name').value()
                nodeToCheck = nuke.toNode(toCheck)

                a = nodeToCheck.dependent()

                if len(a) == 0:
                    nuke.delete(nodeToCheck)

                else:
                    pass
        else:
            pass

        print ('Check 03, After removing solitary reads')

        set_Progress_Bar(1)
        #========================================================================
        # DEFINING THE LOOP TO COPY THE CACHE FILES
        #========================================================================

        def copyLoopGeo(node):


            readsToPopG = GeoToExclude
            if readsToPopG != "":
                readsToPopListG = readsToPopG.split(", ")
            else:
                pass

            listToCopyG = []

            for n in nuke.allNodes(node):
                namen = n.knob('name').value()
                listToCopyG.append(namen)

            lenPopReadsG = len(listToCopyG)
            for m in range(0, int(lenPopReadsG)):

                try:
                    listToCopyG.remove(readsToPopListG[m])
                except:
                    pass

            print (listToCopyG)


            for i in nuke.allNodes(node):

                Geoname = i.knob('name').value()  
                GeoFile = i.knob('file').value()

                if GeoFile == "":
                    continue
                else:
                    pass

                if os.path.isabs(GeoFile) == False:

                    GeoFile = MY_PROJECT_PATH + "/" + GeoFile
                else:

                    pass


                if GeoFile in copiedFilepaths:
                    continue
                else:
                    pass

                if Geoname in copiedNodes:
                    continue
                else:
                    pass

                if Geoname not in listToCopyG:
                    continue
                else:
                    pass


                GeoBaseName = os.path.basename(GeoFile)
                GeoExtension = os.path.splitext(GeoBaseName)
                
                if listToCopyG != "":

                    os.makedirs(DESTINATION+MAINFOLDER+"/Cache/"+str(Geoname))
                    folderToPlaceCopy = DESTINATION+MAINFOLDER+"/Cache/"+str(Geoname)


                    shutil.copy(GeoFile, str(folderToPlaceCopy))
                    copiedNodes.append(Geoname)
                    copiedFilepaths.append(GeoFile)
                    newPath = "Cache/"+str(Geoname)+"/"+str(GeoBaseName)
                    i.knob('file').setValue(newPath)
                    continue

                else:
                    pass


        #================================================================================
        # Creating the Cache folder if required and running the function

        if CopyGeoFiles == True:
            
            os.makedirs(DESTINATION+MAINFOLDER+"/Cache")
            copyLoopGeo('ReadGeo2')
            copyLoopGeo("Camera2")
        else:
            pass

        print ('Check 04, After copy geo')

        set_Progress_Bar(2)
        #================================================================================
        #================================================================================
        #================================================================================

        #Declaring the list of nodes we are going to copy

        listToCopy = []



        # Looping through all the nodes and appending them to the list.

        for n in nuke.allNodes('Read'):
            namen = n.knob('name').value()
            listToCopy.append(namen)

        for nn in nuke.allNodes('DeepRead'):
            namenn = nn.knob('name').value()
            listToCopy.append(namenn)

        for nnn in nuke.allNodes('Group'):

            namennn = nnn.knob('name').value()
            nGroupNode = nuke.toNode(namennn)
            nGroupNode.begin()
            for n in nuke.allNodes('Read'):
                namen = n.knob('name').value()
                listToCopy.append(namen+"_"+namennn)

            for nn in nuke.allNodes('DeepRead'):
                namenn = nn.knob('name').value()
                listToCopy.append(namenn+"_"+namennn)
            nGroupNode.end()            

        # Looking for the nodes the user do not want to copy and removing them from the list

        readsToPop = ReadsToExclude
        if readsToPop != "":
            readsToPopList = readsToPop.split(", ")
        else:
            pass

        lenPopReads = len(listToCopy)
        for m in range(0, int(lenPopReads)):

            try:
                listToCopy.remove(readsToPopList[m])
            except:
                pass

        # Lets close the widget before the Progress Bar

        self.wgADVICE.close()
        self.wgHeader.close()

        print (listToCopy)
        #================================================================================
        # With These Loop we are gonna Copy Each Target Read and create the directories
        #================================================================================

        #To avoid problems with diferent files that have the same name (pls dont do that...)


        def copyReads(readFileR, nameR, nameNumber, insideGroup, groupNameInside):

            #Avoiding errors with empty and relative filepaths

            readFile = readFileR
            name = nameR
            targetNode = nuke.toNode(name)


            if insideGroup == True:
                groupNameInside = groupNameInside
            else:
                pass

            if readFile == "":
                return
            else:
                pass

            if os.path.isabs(readFile) == False:
                
                readFile = MY_PROJECT_PATH + "/" + readFile
            else:
                
                pass

            #READ VARIABLES.
            
            readFilePath = os.path.dirname(readFile)
            readBaseName = os.path.basename(readFile)
            nameExtension = os.path.splitext(readBaseName)
            filename = nameExtension[0]
            fileExtension = nameExtension[1]

            seqList = [".exr", ".dpx", ".jpg", ".png", ".tiff", ".targa", ".jpeg" ]


            #Avoiding to copy Reads already copied.

            if readFile in copiedFilepaths:
                return
            else:
                pass

            if name in copiedNodes:
                return
            else:
                pass

            if insideGroup == False:
                if name not in listToCopy:
                    return
                else:
                    pass
            elif insideGroup== True:
                checkName = name+"_"+groupNameInside
                if checkName not in listToCopy:
                    return
                else:
                    pass

            print ('Check 05, Just Before Normal Read Loop')
    #------------------------------------------------------------------------------------------------------------

            if filename.find(str("%d")) != -1 or  filename.find(str("%02d")) != -1  or  filename.find(str("%03d")) != -1 or  filename.find(str("%04d")) != -1 or filename.find(str("%05d")) != -1 or filename.find(str("%06d")) != -1 or filename.find(str("%07d")) != -1 or filename.find(str("%08d")) != -1 or filename.find(str("####")) != -1:
                if fileExtension in seqList:

                    readFirst = targetNode['first'].value()
                    print ('readFirst: '+str(readFirst))
                    readLast = targetNode['last'].value()
                    print ('readLast: '+str(readLast))
                    print ('filename: ' +str(filename))
                    
                    for e in range(readFirst, readLast+1):
                    
                        if filename.find(str("%d")) != -1:
                            try:
                                readBaseNameFraming = readBaseName.replace("%d", str(e))
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

                        elif filename.find(str("%04d")) != -1:
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

                        fileToCopy = str(readFilePath) +"/"+ str(readBaseNameFraming)

                        if e == readFirst:

                            if filename.find(str("%04d")) != -1:
                                try:
                                    filenameFix = filename.replace("%04d", "")
                                except:
                                    pass
                            elif filename.find(str("%02d")) != -1:
                                try:
                                    filenameFix = filename.replace("%02d", "")
                                except:
                                    pass
                            elif filename.find(str("%03d")) != -1:
                                try:
                                    filenameFix = filename.replace("%03d", "")
                                except:
                                    pass
                            elif filename.find(str("%d")) != -1:
                                try:
                                    filenameFix = filename.replace("%d", "")
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


                            os.makedirs(DESTINATION+MAINFOLDER+"/footage/"+str(filenameFix)+"_"+str(nameNumber))

                            folderToPlaceCopy = DESTINATION+MAINFOLDER+"/footage/"+str(filenameFix)+"_"+str(nameNumber)

                            shutil.copy(str(fileToCopy), str(folderToPlaceCopy))


                        elif e == readLast:

                            shutil.copy(str(fileToCopy), str(folderToPlaceCopy))
                            if insideGroup == False:
                                copiedNodes.append(name)
                            elif insideGroup == True:
                                copiedNodes.append(name+"_"+groupNameInside)
                            else:
                                pass

                            copiedFilepaths.append(readFile)

                            newPath = "footage/"+str(filenameFix)+"_"+str(nameNumber)+"/"+str(readBaseName)
                            targetNode.knob('file').setValue(newPath)

                        else:

                            shutil.copy(str(fileToCopy), str(folderToPlaceCopy))

                            #return
    

            # Ok, if the file is not a image sequence, just copy it. 
            else:
                #print "movie"
                
                try:
                    os.makedirs(DESTINATION+MAINFOLDER+"/footage/"+str(filename)+"_"+str(nameNumber))
                    folderToPlaceCopy = DESTINATION+MAINFOLDER+"/footage/"+str(filename)+"_"+str(nameNumber)
                    
                    shutil.copy(str(readFile), str(folderToPlaceCopy))
                    if insideGroup == False:
                        copiedNodes.append(name)
                    elif insideGroup == True:
                        copiedNodes.append(name+"_"+groupNameInside)
                    else:
                        pass


                    copiedFilepaths.append(readFile)
                    newPath = "footage/"+str(filename)+"_"+str(nameNumber)+"/"+str(readBaseName)
                    targetNode.knob('file').setValue(newPath)
                except:
                    #print "something happened trying to copy a movie"
                    return

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
        nameNumber = 0
        set_Progress_Bar(3)
        for i in nuke.allNodes('Read'):
            nameNumber = nameNumber + 1
            name = i.knob('name').value()
            readFile = i.knob('file').value()
            copyReads(readFile, name, nameNumber, False, "")


        set_Progress_Bar(4)

        for x in nuke.allNodes('DeepRead'):
            nameNumber = nameNumber + 1
            name = x.knob('name').value()
            readFile = x.knob('file').value()
            copyReads(readFile, name, nameNumber, False, "")

        set_Progress_Bar(5)

        for z in nuke.allNodes('Group'):

            GroupName = z.knob('name').value()
            print ('GroupName')
            groupNode = nuke.toNode(GroupName)
            groupNode.begin()

            copyLoopGeo('Camera2')
            copyLoopGeo('ReadGeo2')

            for subZ in nuke.allNodes('Read'):
                nameNumber = nameNumber + 1
                name = subZ.knob('name').value()
                readFile = subZ.knob('file').value()
                print ('name')
                print ('readFile')
                copyReads(readFile, name, nameNumber, True, GroupName)


            for subZZ in nuke.allNodes('DeepRead'):
                nameNumber = nameNumber + 1
                name = subZZ.knob('name').value()
                readFile = subZZ.knob('file').value()
                copyReads(readFile, name, nameNumber, True, GroupName)

            groupNode.end()

        set_Progress_Bar(6)







        #================================================================
        # Deleting Not copied reads if required

        def deletingNotCopiedReads(targetNotCopiedRead):
            for e in nuke.allNodes(targetNotCopiedRead):
                nameToRemove = e.knob('name').value()
                removing = nuke.toNode(nameToRemove)
                if nameToRemove not in copiedNodes:
                    nuke.delete(removing)
                else:
                    pass           

        if RemoveNotCopiedReads == True:
            deletingNotCopiedReads('Read')
            deletingNotCopiedReads('DeepRead')

        else:
            pass

        set_Progress_Bar(7)
        #================================================================
        # Creating the info .txt file!

        newData = nukescripts.get_script_data()
        totalCopied = str(len(copiedNodes))



        date = datetime.datetime.now()
        collectDate = date.strftime("%m/%d/%Y, %H:%M:%S")

        file = open(DESTINATION+MAINFOLDER+"/collected_Info"+MY_PROJECT_NAME+".txt", "w")
        file.write(collectDate + "\n\n\n" + "Total of reads copied:" + totalCopied + "\n\n\n" + "Old Script info:" + "\n\n\n" + OLD_DATA + "\n\n\n\n\n\n\n\n\n" + "New Script info:" + "\n\n\n" + newData )
        file.close()

        #CLOSE THE WIDGET!!
        #self.wgADVICE.close()
        #self.wgHeader.close()


        set_Progress_Bar(8) 
        x = nuke.message('Collect Files Done!')

        if openContainerFolder == True:
            PathToSaveNormalize = PathToSave.replace('/', '\\')

            os.system('explorer %s' % PathToSaveNormalize)
        else:
            pass

def load_mtCollectFiles(ui_load, ui_advise_load):
    global tool 
    ui = ui_load
    ui_advise = ui_advise_load
    tool = mtCollectFiles(ui, ui_advise)



