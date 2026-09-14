#                            # #######################################                          #
#                            #                                       #                          #
#                            #          Author: Miguel Torija        #                          #
#                            #                                       #                          #
#                            # #######################################                          #
#                                                                                               #
#                            # Created by: Miguel Torija                                        #
# -------------------------- #         mt Collect Utilities   ----------------------------------#  
#                            #    

"""
======================================================================================
# Tool Name      : <mt Collect Utilities>
# Version        : 1.0.0
"""

__title__ = 'mt Collect Utilities'
__version__ = "1.0.0"
__author__ = "Miguel Torija"
__release_date__ = 'Jan, 21 2026'


#  python tools modified by Nitin Kashyap #
__pythonFix_Debug__= "Nitin Kashyap"
__Add_menu_py__= "Nitin Kashyap"
__tools_modified__= "Nitin Kashyap"
__Niitn_Kashyap__ = "Nitin Kashyap"
__fix_update_date__tools_ = "Nitin Kashyap"





import nuke
import os
import datetime


version= "v1.0.0"
update_date= "20 Jan 2026"


import nuke, sys, os



dotNukeFolder = os.path.expanduser(
    "~/.nuke/CollectUtilities_v3/CollectUtilities_v03_scripts"
)

if dotNukeFolder not in sys.path:
    sys.path.append(dotNukeFolder)

# UI folder
ui_dir = os.path.join(dotNukeFolder, "ui")

m = nuke.menu("Nodes").addMenu("Collect Utilities", icon="icon_mtCollectUtilities_v03.png")

m.addCommand("Check Frames", "import mtCheckFrames; mtCheckFrames.mtCheckFrames()")

m.addCommand(
    "Files To Folder",
    "import os; from mtFilesToFolder_v03 import load_mtFilesToFolder; "
    "load_mtFilesToFolder(os.path.expanduser('~/.nuke/CollectUtilities_v3/CollectUtilities_v03_scripts/ui/mtFilesToFolder_v001.ui'))"
)

m.addCommand(
    "File Renamer",
    "import os; from mtFileRenamer_v03_1 import load_mtFileRenamer; "
    "load_mtFileRenamer(os.path.expanduser('~/.nuke/CollectUtilities_v3/CollectUtilities_v03_scripts/ui/mtFileRenamer_v001.ui'))"
)

m.addCommand(
    "Collect Files",
    "import os; from mtCollectFiles_v03 import load_mtCollectFiles; "
    "base=os.path.expanduser('~/.nuke/CollectUtilities_v3/CollectUtilities_v03_scripts/ui/'); "
    "load_mtCollectFiles(base+'mtCollectFiles_v002.ui', base+'mtCollectFiles_advise_v001.ui')"
)

m.addCommand("Get Frames", "import mtGetFrames; mtGetFrames.mtGetFrames()")




license ="Copyright (C) 2025 by Nitin Kashyap,All rights reserved."
nuke.tprint(f"CollectUtilities {version},  build  {update_date}. \n{license}")