import shutil, os, nuke, nukescripts, threading, time, datetime
import nuke

def mtGetFrames():
    myProjectRoot = nuke.root().knob('name').value()
    myProject = os.path.basename(myProjectRoot)
    myRoot = os.path.dirname(myProjectRoot)
    myProjectcut = myProject[0:-3]

    try:
        targetRead = nuke.selectedNode()
    except:
        nuke.message('Ups! You must select one Read please (only one)')
        return  # exit if no node selected

    if not targetRead or targetRead.Class() != "Read":
        nuke.message('Ups! You must select one Read please (only one)')
        return

    # safe to use targetRead now


    seqList = [".exr", ".dpx", ".jpg", ".png", ".tiff", ".targa", ".jpeg"]

    targetReadColorspace = targetRead.knob('colorspace').value()

    if targetReadColorspace == "default (linear)":
        targetReadColorspace = 0
    else:
        pass

    targetReadFormat = targetRead.knob('format').value()
    targetReadFile = targetRead.knob('file').value()

    readFilePath = os.path.dirname(targetReadFile)
    readBaseName = os.path.basename(targetReadFile)
    nameExtension = os.path.splitext(readBaseName)
    filename = nameExtension[0]
    fileExtension = nameExtension[1]

    if os.path.isabs(targetReadFile) == False:
        targetReadFile = myRoot + "/" + targetReadFile
    else:
        pass

    p = nuke.Panel('Take Frames')
    p.addEnumerationPulldown('method', 'All Custom')
    p.addSingleLineInput('Custom Frames', '')
    p.addBooleanCheckBox('Auto order reads', True)

    if p.show() == True:

        framesToTake = p.value('Custom Frames')
        framesToTakeList = framesToTake.split(", ")
        print(framesToTakeList)

        framesToTakeListGOOD = []
        methodValue = p.value('method')
        print(methodValue)

        if methodValue == 'Custom':
            for frames in framesToTakeList:
                if frames.find(str("-")) != -1:
                    print("oh yeah")
                    sandia = frames.split("-")
                    tinto = int(sandia[0])
                    verano = int(sandia[1])
                    vasos = abs(tinto - verano)
                    for hielos in range(0, vasos+1):
                        borrachos = tinto + hielos
                        framesToTakeListGOOD.append(borrachos)
                else:
                    print("oh no")
                    framesToTakeListGOOD.append(frames)

        elif methodValue == 'All':
            print('yes')
            tinto = int(targetRead.knob('first').value())
            verano = int(targetRead.knob('last').value())
            for z in range(tinto, (verano+1)):
                print(z)
                framesToTakeListGOOD.append(z)
        else:
            pass

        print(framesToTakeListGOOD)
        toSelectReads = []

        for i in framesToTakeListGOOD:
            if filename.find(str("%d")) != -1 or filename.find(str("%02d")) != -1 or filename.find(str("%03d")) != -1 or filename.find(str("%04d")) != -1 or filename.find(str("%05d")) != -1 or filename.find(str("%06d")) != -1 or filename.find(str("####")) != -1:
                if fileExtension in seqList:

                    newRead = nuke.createNode('Read')
                    newReadName = newRead.knob('name').value()
                    newRead.knob('colorspace').setValue(targetReadColorspace)
                    newRead.knob('first').setValue(int(i))
                    newRead.knob('last').setValue(int(i))
                    newRead.knob('on_error').setValue("black")
                    newRead.knob('format').setValue(targetReadFormat)

                    if filename.find(str("%04d")) != -1:
                        try:
                            if len(str(i)) < 4:
                                badLen = len(str(i))
                                difLen = 4 - badLen
                                multLen = '0' * difLen
                                fixNum = multLen + str(i)
                            else:
                                fixNum = i
                            readBaseNameFraming = readBaseName.replace("%04d", str(fixNum))
                        except:
                            pass

                    elif filename.find(str("%d")) != -1:
                        try:
                            readBaseNameFraming = readBaseName.replace("%d", str(i))
                        except:
                            pass

                    elif filename.find(str("%02d")) != -1:
                        try:
                            if len(str(i)) < 2:
                                badLen = len(str(i))
                                difLen = 2 - badLen
                                multLen = '0' * difLen
                                fixNum = multLen + str(i)
                            else:
                                fixNum = i
                            readBaseNameFraming = readBaseName.replace("%02d", str(fixNum))
                        except:
                            pass

                    elif filename.find(str("%03d")) != -1:
                        try:
                            if len(str(i)) < 3:
                                badLen = len(str(i))
                                difLen = 3 - badLen
                                multLen = '0' * difLen
                                fixNum = multLen + str(i)
                            else:
                                fixNum = i
                            readBaseNameFraming = readBaseName.replace("%03d", str(fixNum))
                        except:
                            pass

                    elif filename.find(str("%05d")) != -1:
                        try:
                            if len(str(i)) < 5:
                                badLen = len(str(i))
                                difLen = 5 - badLen
                                multLen = '0' * difLen
                                fixNum = multLen + str(i)
                            else:
                                fixNum = i
                            readBaseNameFraming = readBaseName.replace("%05d", str(fixNum))
                        except:
                            pass

                    elif filename.find(str("%06d")) != -1:
                        try:
                            if len(str(i)) < 6:
                                badLen = len(str(i))
                                difLen = 6 - badLen
                                multLen = '0' * difLen
                                fixNum = multLen + str(i)
                            else:
                                fixNum = i
                            readBaseNameFraming = readBaseName.replace("%06d", str(fixNum))
                        except:
                            pass

                    elif filename.find(str("####")) != -1:
                        try:
                            readBaseNameFraming = readBaseName.replace("####", str(i))
                        except:
                            pass
                    else:
                        pass

                    targetFrameToTake = str(readFilePath) + "/" + str(readBaseNameFraming)
                    newRead.knob('file').setValue(targetFrameToTake)
                    toSelectReads.append(newReadName)

    if p.value('Auto order reads') == 1:
        targetRead.setSelected(False)
        for i in toSelectReads:
            x = nuke.toNode(i)
            x.setSelected(True)
        ojoo = nuke.selectedNodes()
        for lol in ojoo:
            nuke.autoplace(lol)