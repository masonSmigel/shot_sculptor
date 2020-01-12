#==========================================================================================
#
#MS-Shot-Sculptor
#
#==========================================================================================
# 
#  version 0.01     12/15/19
#
#    Author: Mason Smigel
#    
#    email: mgsmigel@gmail.com
#
#------------------------------------------------------------------------------------------
#    
#------------------------------------------------------------------------------------------
# 
#    DESCRIPTION 
#    
#    MS-Shot-Sculpt creates, edits and animates tangentspace blendshapes across skinned meshes.
#    It stores all the animation, mesh and blendshape data in a single Shot-Sculpt Node (DO NOT DELETE IT!!!!)
#    
#    
#    INSTALL
#
#    1. Move the MS_ShotSculptor.py file to your maya scripts directory. 
#
#        found at:
#                 MAC :/Users/<user>/Library/Preferences/Autodesk/maya/scripts
#                 WIN: <drive>:\\Documents\\maya\\scripts
#
#
#    2. Move the MS_shotSculptor_Icon.png to your maya icons directory
#
#    found at:
#             MAC :/Users/<user>/Library/Preferences/Autodesk/maya/<version>/prefs/icons
#             WIN: <drive>:\Documents\\maya\<version>\prefs\icons
#                 
#    3. Restart maya if it is currently running. 
#
#    4. select the shelf you would like to add the button to. Drag and drop the install.py file into maya 
#   
#                ----------------------- OR -----------------------
#                
#                
#    1. Open the MS_ShotSculptor.py in a python tab of the script editor
#    
#    2. Run the script
#    
#    
#   
#    USAGE- 
#    
#    
#    1. Select all Skinned Meshes you wish to influence and press "Create Shot-Sculpt Group". 
#    
#    2. Move to the frame you want to correct and press "Create Sculpt-Frame"
#    
#    3. Use any sculpting and modeling tools (NO DEFORMERS) to sculpt your corrective. 
#            
#    4. Press the Edit button to exit edit mode. 
#    
#------------------------------------------------------------------------------------------
#
#==========================================================================================


import pymel.core as pm 

def onMayaDroppedPythonFile(*args, **kwargs):
    current_shelf = pm.mel.eval("shelfTabLayout -query -selectTab $gShelfTopLevel")
    
    pm.shelfButton( i = 'MS_shotSculptor_Icon.png', 
                p = current_shelf,
                sourceType = 'python', 
                label = 'MS-Shot-Sculptor',
                c= "import MS_ShotSculptor; reload(MS_ShotSculptor)",
                ann = "Open MS-Shot-Sculptor" )