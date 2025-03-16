# MS_ShotSculptor
Corrective shot sculpting tool for maya. 


  version 0.01     12/15/19

  Author: Mason Smigel
    
  email: mgsmigel@gmail.com

  version 1.5     16/12/24   Adaptation to Python 3, Maya (2022+)    
 
  Contributor : Clement Daures

  email: clementdaures.contact@gmail.com

------------------------------------------------------------------------------------------

It appears that PyMEL is no longer supported in Maya 2025 and later versions. Clement Daures is currently developing version 2.0 of ShotSculptor, which will utilize vanilla Python (cmds), MEL, and OpenMaya commands.

------------------------------------------------------------------------------------------
    
 
    DESCRIPTION 
    
    MS-Shot-Sculpt creates, edits and animates tangent space blendshapes across skinned meshes.
    It stores all the animation, mesh and blendshape data in a single Shot-Sculpt Node (DO NOT DELETE IT!!!!)
   
    
    INSTALL

  ## For Maya 2022 and Above (Python 3 Compatible)

    1. Move the ShotSculptor_Py3_Compatible/scripts/MS_ShotSculptor_PY3.py file to your maya scripts directory. 

        found at:
                 MAC :/Users/<user>/Library/Preferences/Autodesk/maya/scripts
                 WIN: <drive>:\\Documents\\maya\\<version>\\scripts


    2. Move the ShotSculptor_Py3_Compatible/icons/MS_shotSculptor_Icon.png to your maya icons directory

    	found at:
             MAC :/Users/<user>/Library/Preferences/Autodesk/maya/<version>/prefs/icons
             WIN: <drive>:\\Documents\\maya\\<version>\\prefs\\icons
                 
    3. Restart maya if it is currently running. 

    4. select the shelf you would like to add the button to. Drag and drop the ShotSculptor_Py3_Compatible/install_PY3.py file into maya 
   
                ----------------------- OR -----------------------
                
                
    1. Open the MS_ShotSculptor.py in a python tab of the script editor
    
    2. Run the script
    
  ## For Maya 2022 and Below (Python 2 Compatible)

    1. Move the ShotSculptor_Py2_Compatible/scripts/MS_ShotSculptor_PY2.py file to your maya scripts directory. 

        found at:
                 MAC :/Users/<user>/Library/Preferences/Autodesk/maya/scripts
                 WIN: <drive>:\\Documents\\maya\\<version>\\scripts


    2. Move the ShotSculptor_Py2_Compatible/icons/MS_shotSculptor_Icon.png to your maya icons directory

    	found at:
             MAC :/Users/<user>/Library/Preferences/Autodesk/maya/<version>/prefs/icons
             WIN: <drive>:\\Documents\\maya\\<version>\\prefs\\icons
                 
    3. Restart maya if it is currently running. 

    4. select the shelf you would like to add the button to. Drag and drop the ShotSculptor_Py2_Compatible/install_PY2.py file into maya 
   
                ----------------------- OR -----------------------
                
                
    1. Open the MS_ShotSculptor.py in a python tab of the script editor
    
    2. Run the script  
  

  USAGE 
    
    
    1. Select all Skinned Meshes you wish to influence and press "Create Shot-Sculpt Group". 
    
    2. Move to the frame you want to correct and press "Create Sculpt-Frame"
    
    3. Use any sculpting and modeling tools (NO DEFORMERS) to sculpt your corrective. 
            
    4. Press the Edit button to exit edit mode. 
    
