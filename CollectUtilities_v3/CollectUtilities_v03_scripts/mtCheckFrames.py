import os, sys, shutil
import nuke


def mtCheckFrames():
    p = nuke.Panel('Missing Frames')

    p.addEnumerationPulldown('Frame Range', 'Read Project Custom')

    p.addSingleLineInput('Custom First', 1001)
    p.addSingleLineInput('Custom Last', 1100)
     
    try:
        readNode = nuke.selectedNode()
        readFile = readNode.knob('file').value()
        readFilePath = os.path.dirname(readFile)
        readBaseName = os.path.basename(readFile)
        nameExtension = os.path.splitext(readBaseName)
        filename = nameExtension[0]
        fileExtension = nameExtension[1]

        if os.path.isabs(readFile) == False:

            myProjectRoot = nuke.root().knob('name').value()
            myRoot = os.path.dirname(myProjectRoot)
            readFile = myRoot + "/" + readFile
            readFilePath = os.path.dirname(readFile)
            readBaseName = os.path.basename(readFile)
            nameExtension = os.path.splitext(readBaseName)
            filename = nameExtension[0]
            fileExtension = nameExtension[1]

        if p.show() == True:

            numberOfMissingFrames = 0
            missingFrames = []

            frOption = p.value('Frame Range')

            customFirst = p.value('Custom First')
            customLast = p.value('Custom Last')

            if frOption == 'Read':

                firstFrame = readNode.knob('first').getValue()

                lastFrame = readNode.knob('last').getValue()

            elif frOption == 'Project':

                firstFrame = nuke.root()['first_frame'].value()
                lastFrame = nuke.root()['last_frame'].value() 
                
            elif frOption == 'Custom':

                firstFrame = customFirst
                lastFrame = customLast

            else:

                firstFrame = 1001
                lastFrame = 1001

            print (firstFrame)
            print (lastFrame)

            seqList = [".exr", ".dpx", ".jpg", ".png", ".tiff", ".targa", ".jpeg"]


            if filename.find(str("%d")) != -1 or filename.find(str("%02d")) != -1  or  filename.find(str("%03d")) != -1 or filename.find(str("%04d")) != -1 or filename.find(str("%05d")) != -1 or filename.find(str("%06d")) != -1 or filename.find(str("%07d")) != -1 or filename.find(str("####")) != -1:

                if fileExtension in seqList:

                    print ('check 1')
                    for e in range(int(firstFrame), (int(lastFrame)+1)):

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
                                readBaseNameFraming = readBaseName.replace("%07d", str(fixnum))
                            except:
                                pass

                        elif filename.find(str("####")) != -1:
                            try:
                                readBaseNameFraming = readBaseName.replace("####", str(e))
                            except:
                                pass
                        else:
                            pass


                        fileToSearch = str(readFilePath) +"/"+ str(readBaseNameFraming)
                        print (fileToSearch)
                        try: 
                            if os.path.isfile(fileToSearch):
                                print ('everything good')
                                pass
                            else:
                                print ('woops, frame missing')
                                numberOfMissingFrames = numberOfMissingFrames + 1
                                missingFrames.append(e)
                        except:
                            print ('algo ha pasao')
                            continue
            else:
                pass
            nuke.message('The following frames are missing: {} \n \nThat makes a total of "{}" frames missing.'.format(missingFrames, numberOfMissingFrames))


        else:
            pass
    except:
        nuke.message ('You must have selected a Read Node') 