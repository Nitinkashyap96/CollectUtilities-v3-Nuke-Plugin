import shutil, nuke, os, nukescripts, threading, time, datetime, psutil
import webbrowser



from PySide2 import QtWidgets, QtCore, QtUiTools

#*********************************************************************

class mtFileRenamer:

    def __init__(self, ui):


        try:
            x = nuke.selectedNode()
        except:
            nuke.message('you must select a Read node')
            return
        path_ui = ui
        #path_ui = "C:/Users/Usuario/.nuke/CollectUtilities_v3/ui/mtFileRenamer_v001.ui"

        myProjectRoot = nuke.root().knob('name').value()

        myProject = os.path.basename(myProjectRoot)
        myRoot = os.path.dirname(myProjectRoot)
        myProjectcut = myProject[0:-3]
        targetRead = nuke.selectedNode()

        targetReadFile = targetRead.knob('file').value()

        if os.path.isabs(targetReadFile) == False:
            
            targetReadFile = myRoot + "/" + targetReadFile
        else:
            
            pass

        readFilePath = os.path.dirname(targetReadFile)
        readBaseName = os.path.basename(targetReadFile)
        nameExtension = os.path.splitext(readBaseName)
        filename = nameExtension[0]
        fileExtension = nameExtension[1]
    


        self.wgRenamer = QtUiTools.QUiLoader().load(path_ui)

        # SETUP ---------------
        self.wgRenamer.lblCurrentName.setText(filename)


        # MAIN SIGNALS ---------------
        self.wgRenamer.btnRename.clicked.connect(self.press_btnRENAME)
        # Other Signals
        self.wgRenamer.btnWEB.clicked.connect(self.press_btnWEB)
        self.wgRenamer.btnInfo.clicked.connect(self.press_btnInfo)


        # RUN ---------------
        self.wgRenamer.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.wgRenamer.show()

    #*********************************************************************
    # PRESS
    def press_btnInfo(self):
        webbrowser.open("https://www.migueltorija.com/post/user-guide-mtcollect-utilities-v3-0")

    def press_btnWEB(self):
        webbrowser.open("https://www.migueltorija.com/")

    def press_btnRENAME(self):

        newName = self.wgRenamer.lineEditNewName.text()
        print (newName)
        changeAllNames = self.wgRenamer.cbChangePathAll.isChecked()

        changeFirstFrame = self.wgRenamer.cbChangeFirstFrame.isChecked()

        newStartFrame = self.wgRenamer.spinBoxNewFirstFrame.value()





        myProjectRoot = nuke.root().knob('name').value()

        myProject = os.path.basename(myProjectRoot)
        myRoot = os.path.dirname(myProjectRoot)
        myProjectcut = myProject[0:-3]
        targetRead = nuke.selectedNode()

        targetReadFile = targetRead.knob('file').value()

        if os.path.isabs(targetReadFile) == False:
            
            targetReadFile = myRoot + "/" + targetReadFile
        else:
            
            pass

        readFilePath = os.path.dirname(targetReadFile)
        readBaseName = os.path.basename(targetReadFile)
        nameExtension = os.path.splitext(readBaseName)
        filename = nameExtension[0]
        fileExtension = nameExtension[1]

        self.wgRenamer.hide()
        if nuke.ask('This action will overwritte the old file and can not be undone. Do you want to continue?'):
            self.wgRenamer.show()


            readFirstFrame = int(targetRead.knob('first').value())
            readLastFrame = int(targetRead.knob('last').value())

            print (readFirstFrame)
            print (readLastFrame)


            seqList = [".exr", ".dpx", ".jpg", ".png", ".tiff", ".targa", ".jpeg" ]

            
            if filename.find(str("%d")) != -1 or  filename.find(str("%02d")) != -1 or filename.find(str("%03d")) != -1 or filename.find(str("%04d")) != -1 or filename.find(str("%05d")) != -1 or filename.find(str("%06d")) != -1 or filename.find(str("%07d")) != -1 or filename.find(str("%08d")) != -1 or filename.find(str("####")) != -1:
                if fileExtension in seqList:
                    print ('Sequence')


                    for i in range(readFirstFrame, readLastFrame+1):
                        print (i)
                        if filename.find(str("%d")) != -1:
                            print ('pad 1')
                            try:
                                readBaseNameFraming = readBaseName.replace("%d", str(i))
                                newPadding = "%d"
                                print ("newFrameChanged: "+str(newFrameChanged))
                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)

                            except:
                                print ('fail to change')
                                pass

                        elif filename.find(str("%02d")) != -1:
                            print ('pad 2')
                            try:
                                if len (str(i))<2:
                                    badLen = len(str(i))
                                    difLen = 2 - badLen
                                    multLen = '0'*difLen
                                    fixNum = multLen+str(i)
                                else:
                                    fixNum = i
                                    pass

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("%02d", str(fixNum))
                                newPadding = "%02d"
                            except:
                                print ('fail to change')
                                pass

                        elif filename.find(str("%03d")) != -1:
                            print ('pad 3')
                            try:
                                if len (str(i))<3:
                                    badLen = len(str(i))
                                    difLen = 3 - badLen
                                    multLen = '0'*difLen
                                    fixNum = multLen+str(i)
                                else:
                                    fixNum = i
                                    pass

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("%03d", str(fixNum))
                                newPadding = "%03d"
                            except:
                                print ('fail to change')
                                raise
                                pass                                    

                        elif filename.find(str("%04d")) != -1:
                            print ('pad 4')
                            try:
                                if len (str(i))<4:
                                    badLen = len(str(i))
                                    difLen = 4 - badLen
                                    multLen = '0'*difLen
                                    fixNum = multLen+str(i)
                                else:
                                    fixNum = i
                                    pass

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("%04d", str(fixNum))
                                newPadding = "%04d"
                            except:
                                print ('fail to change')
                                pass

                        elif filename.find(str("%05d")) != -1:
                            print ('pad 5')
                            try:
                                if len (str(i))<5:
                                    badLen = len(str(i))
                                    difLen = 5 - badLen
                                    multLen = '0'*difLen
                                    fixNum = multLen+str(i)
                                else:
                                    fixNum = i
                                    pass

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("%05d", str(fixNum))
                                newPadding = "%05d"
                            except:
                                print ('fail to change')
                                pass

                        elif filename.find(str("%06d")) != -1:
                            print ('pad 6')
                            try:
                                if len (str(i))<6:
                                    badLen = len(str(i))
                                    difLen = 6 - badLen
                                    multLen = '0'*difLen
                                    fixNum = multLen+str(i)
                                else:
                                    fixNum = i
                                    pass

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("%06d", str(fixNum))
                                newPadding = "%06d"
                            except:
                                print ('fail to change')
                                pass

                        elif filename.find(str("%07d")) != -1:
                            print ('pad 7')
                            try:
                                if len (str(i))<7:
                                    badLen = len(str(i))
                                    difLen = 7 - badLen
                                    multLen = '0'*difLen
                                    fixNum = multLen+str(i)
                                else:
                                    fixNum = i
                                    pass

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("%07d", str(fixNum))
                                newPadding = "%07d"
                            except:
                                print ('fail to change')
                                pass

                        elif filename.find(str("%08d")) != -1:
                            print ('pad 8')
                            try:
                                if len (str(i))<8:
                                    badLen = len(str(i))
                                    difLen = 8 - badLen
                                    multLen = '0'*difLen
                                    fixNum = multLen+str(i)
                                else:
                                    fixNum = i
                                    pass

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("%08d", str(fixNum))
                                newPadding = "%08d"
                            except:
                                print ('fail to change')
                                pass


                        elif filename.find(str("####")) != -1:
                            try:

                                DIFnewFrameChanged = readFirstFrame-newStartFrame
                                newFrameChanged = i - (DIFnewFrameChanged)
                                print ("newFrameChanged: "+str(newFrameChanged))
                                readBaseNameFraming = readBaseName.replace("####", str(i))
                                newPadding = "####"
                            except:
                                print ('fail to change')
                                pass
                        else:
                            pass




                        if changeFirstFrame == False:

                            print ("No Change First Frame")

                            readFileSearch = readFilePath + '/' + readBaseNameFraming

                            newFile = readFilePath + '/'+ newName + '.' + str(fixNum) + fileExtension

                            print ("newFile: "+newFile)

                            print ("readFileSearch: "+readFileSearch)

                            shutil.move(readFileSearch, newFile)


                        elif changeFirstFrame == True:

                            print ("Change First Frame")

                            readFileSearch = readFilePath + '/' + readBaseNameFraming

                            newFile = readFilePath + '/'+ newName + '.' + str(newFrameChanged) + fileExtension

                            print ("newFile: "+newFile)

                            print ("readFileSearch: "+readFileSearch)

                            shutil.move(readFileSearch, newFile)

                        else:
                            pass


#FIN DEL LOOP-----------------------------------------------------------------------------
                    print ('end of the loop')
                    if changeFirstFrame == False:
                        newFilePath = readFilePath + '/'+newName + '.' + newPadding + fileExtension
                        targetRead.knob('file').setValue(newFilePath)


                        if changeAllNames == True:
                            anakin = nuke.allNodes('Read')

                            for jedi in anakin:
                                luke = jedi.knob('file').value()
                                if luke == targetReadFile:
                                    jedi.knob('file').setValue(newFilePath)

                        else:
                            pass



                    elif changeFirstFrame == True:

                        totalFrames = readLastFrame-readFirstFrame
                        toFindPadding = newStartFrame+totalFrames
                             

                        if toFindPadding == 3:
                            newPadding = "%03d"
                        elif toFindPadding == 1:
                            newPadding = "%d"                           
                        elif toFindPadding == 2:
                            newPadding = "%02d"
                        elif toFindPadding == 4:
                            newPadding = "%04d"
                        elif toFindPadding == 5:
                            newPadding = "%05d"
                        elif toFindPadding == 6:
                            newPadding = "%06d"                        
                        elif toFindPadding == 7:
                            newPadding = "%07d"
                        elif toFindPadding == 8:
                            newPadding = "%08d"
                        elif toFindPadding == 9:
                            newPadding = "%09d"

                        readLastFrameNEW=toFindPadding
                        newFilePath = readFilePath + '/'+newName + '.' + newPadding + fileExtension
                        targetRead.knob('file').setValue(newFilePath)
                        targetRead.knob('first').setValue(newStartFrame)
                        targetRead.knob('last').setValue(readLastFrameNEW)


                    if changeAllNames == True:
                        anakin = nuke.allNodes('Read')

                        for jedi in anakin:
                            luke = jedi.knob('file').value()
                            if luke == targetReadFile:
                                jedi.knob('file').setValue(newFilePath)
                                jedi.knob('first').setValue(newStartFrame)
                                jedi.knob('last').setValue(readLastFrameNEW)
                    else:
                        pass




                else:
                    pass



            else:
                print ('No sequence')
                readFile = targetRead.knob('file').value()

                newFile = readFilePath + '/'+newName + fileExtension

                print (newFile)

                shutil.move(readFile, newFile)

                targetRead.knob('file').setValue(newFile)



        else:
            print ('nope')
            pass



def load_mtFileRenamer(ui_load):
    global tool
    ui = ui_load 
    tool = mtFileRenamer(ui)