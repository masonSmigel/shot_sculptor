# -*- coding: UTF-8-*-
#
#==========================================================================================
#
#MS-Shot-Sculptor
#
#==========================================================================================
# 
#  version 0.01     12/15/19
#  version 0.02     1/28/20
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
#------------------------------------------------------------------------------------------
#
#==========================================================================================

import pymel.core as pm


def editIntFeild(intFeild, amt):
    currentVal = pm.intField(intFeild, q=True, v = True)
    newVal = currentVal + amt
    if newVal >= 0:
        pm.intField(intFeild, e=True, v = newVal)
                
def createShotSculptNode():
    
    sel = pm.ls(sl=True)
    
    selSize = len(sel)
    
    pm.textScrollList("SculptLayers_tsl", e=True, ra=True)
    pm.textFieldGrp("selectedSSNode_tfg", e =True,text = "No Active Shot-Sculpt group")

    ##Run error Checks
    if selSize < 1:
        pm.error("MS Shot-Sculptor: " +"no objects selected")
    for s in sel:
        if pm.filterExpand(sm=12, fp=True) == None:  # @UndefinedVariable
            pm.error("MS Shot-Sculptor: " + s + " is not a mesh object. Cannot create a Shot-Sculpt Group.", noContext=True)
           
        
        
        shapes = pm.listRelatives(s, shapes = True)
        if shapes ==[]:
            pm.error("MS Shot-Sculptor: " + s + "is not a Mesh object. Cannot add to Shot-Sculpt group.", noContext = True)
    
    
    ##get the name of the new node
    result = pm.promptDialog(
                title='create Shot Sculpt Node',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')   
    
    if result == 'OK':
        name  = pm.promptDialog(q=True, t =True)
        ssn = pm.group(em=True, n = name + "_ShotSculpt" )
        
        ##TODO setup the SSnode
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy','sz', 'v']:
            channel  = ssn + "." + attr
            pm.setAttr(channel, l=True, k=False ,cb =False)

        pm.addAttr (ssn, longName = "SSN_ID", k=False)
        pm.setAttr (ssn + ".SSN_ID", cb=False)
        
        ##store the influence objects and blendshapes
        pm.addAttr(longName = "influenceObjs" ,dt = "stringArray" ,k = False )
        pm.addAttr(longName = "bshps" ,dt = "stringArray" ,k = False )    
        
        pm.addAttr(ssn, longName = "envelope", at = "float" , hasMinValue =True, min = 0,  hasMaxValue = True, max = 1, k=True, dv = 1)
    
        selArray = []
        BshpsArray = []
        
        for i in range(selSize):
            ##add the selection to the array
            selArray.append(sel[i])
            
            bshpName = sel[i]  + "_"+ ssn  + "_bshp"
            ##create a blendshape
            pm.blendShape(sel[i],n = bshpName, after = True, tangentSpace =True )  # @UndefinedVariable
            BshpsArray.append(bshpName)
            
            pm.connectAttr(ssn + ".envelope" , BshpsArray[i]+ ".envelope" )

        pm.setAttr(ssn + '.influenceObjs', selArray )
        pm.setAttr(ssn + '.bshps', BshpsArray )
        
        ##update the UI 
        pm.textFieldGrp("selectedSSNode_tfg", e =True, text = ssn)  

def autoKey(attr, time):
    

    ##Get attrs from ui 
    easeInFrames =  pm.intField("EaseInIntFeild" , q=True, v = True)
    holdInFrames =  pm.intField("HoldInIntFeild" , q=True, v = True)
    holdOutFrames = pm.intField("HoldOutIntFeild", q=True, v = True)
    easeOutFrames = pm.intField("EaseOutIntFeild", q=True, v = True)
    
    InTangentType = pm.optionMenu("EaseInTangetType_optmenu", q=True, v=True)
    OutTangentType = pm.optionMenu("EaseOutTangetType_optmenu", q=True, v=True)

    
    pm.cutKey(attr, t = ":")  # @UndefinedVariable
    
    initKey =  pm.setKeyframe(attr, v=1, t =time, inTangentType = InTangentType, outTangentType = OutTangentType  )  # @UndefinedVariable
    
    if easeInFrames > 0: 
        pm.setKeyframe(attr,v =0 , t= [time - easeInFrames], outTangentType  = InTangentType) ##ease in @UndefinedVariable
    else:
        initKey
    
    if holdInFrames > 0:
        pm.setKeyframe(attr,v = 1 , t = (time -holdInFrames ), inTangentType =  InTangentType, outTangentType  = InTangentType) ##inHold @UndefinedVariable
    else: 
        initKey
        
    if holdOutFrames > 0:
        pm.setKeyframe(attr,v = 1, t = (time +holdOutFrames ), inTangentType =  OutTangentType, outTangentType  = OutTangentType) ##outHold @UndefinedVariable
    else: 
        initKey
     
    if  easeOutFrames> 0 :        
        pm.setKeyframe(attr,v =0 , t= [time + easeOutFrames], inTangentType = OutTangentType) ##ease out @UndefinedVariable
    else: 
        initKey
          
def loadShotSculptNode():
    sel = pm.ls(sl=True)
    
    pm.textScrollList("SculptLayers_tsl", e=True, ra=True)
    pm.textFieldGrp("selectedSSNode_tfg", e =True,text = "No Active Shot-Sculpt group")
    
    
    if len(sel) > 0:
        if pm.attributeQuery('SSN_ID', node = sel[0], exists =True):  # @UndefinedVariable
            pm.textFieldGrp("selectedSSNode_tfg", e =True, text = sel[0])
            
            ## TODO Load all Sculpt Frames
            attr_list = pm.listAttr(sel[0], k=True)  # @UndefinedVariable
            
            attr_list.remove('envelope')
            
            pm.textScrollList("SculptLayers_tsl", e=True, append =  attr_list )
            
        else: 
            pm.error("MS Shot-Sculptor: " +"Selection is not a Shot Sculpt Node")
    else: 
        pm.warning("MS Shot-Sculptor: " +"Nothing selected")
         
editState = False       
def createSculptFrame():
    
    if editState:
        editSculptFrame()
    
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)  
    
    influence_objs = pm.getAttr(ssn + '.influenceObjs')
    bshps =  pm.getAttr(ssn + '.bshps')
    
    
    pm.textFieldGrp("selectedSSNode_tfg", e = True,text = ssn)
    if ssn == "No Active Shot-Sculpt node":
        pm.error("MS Shot-Sculptor: " +" please create or load a Shot Sculpt Node")
          
    ##create a new tangentSpace blendshapes
    
    time =  int(pm.currentTime())
    frameName = "frame_" + str(time) 
    ssnFrameAttr = ssn + "." + frameName
        
    if pm.attributeQuery(frameName, n = ssn, ex =True):  # @UndefinedVariable
        pm.warning("MS Shot-Sculptor: " +" A  Sculpt-Frame already exists on frame " + str(time) + ". Entering Edit mode instead")
        pm.textScrollList("SculptLayers_tsl", e = True, si = 'frame_' + str(time) )
        editSculptFrame(); return
    
    pm.addAttr(ssn, longName = frameName, at = "float", hasMinValue =True, min = 0,  hasMaxValue = True, max = 1, k=True,  dv = 1 )
    
   
    ##add new frame attr to the UI 
    list_amt = pm.textScrollList("SculptLayers_tsl", q=True, ni=True)
    list_index = list_amt + 1
    pm.textScrollList("SculptLayers_tsl", e=True, appendPosition = [list_index, frameName], showIndexedItem = list_index, selectItem = frameName )

    
    for i in range(len(influence_objs)):
                          
        ##create a new Blendshape and connect all attrs to SSN                      
        bshpIndex = pm.blendShape(bshps[i], q=True, wc=True)  # @UndefinedVariable
                       
        ##create a temporary targetObj
        bshp_target = pm.duplicate(influence_objs[i])
        
        pm.blendShape(bshps[i], edit=True, tangentSpace =True, t =[ influence_objs[i], bshpIndex , bshp_target[0], 1])        # @UndefinedVariable
        pm.aliasAttr(frameName,  bshps[i] + '.w['+ str(bshpIndex) +']')  # @UndefinedVariable
        
        ##delete the tempory obj
        pm.delete(bshp_target)
        
        pm.connectAttr(ssnFrameAttr , bshps[i] +  "." + frameName)
                
    autoKey(ssnFrameAttr, pm.currentTime() )
    editSculptFrame()
       
def getIndexByName(blsNode, targetName):
    attr = blsNode + '.w[{}]'
    weightCount = pm.blendShape(blsNode, q=True, wc=True)  # @UndefinedVariable
    for index in xrange(weightCount):
        if pm.aliasAttr(attr.format(index), q=True) == targetName:  # @UndefinedVariable
            return index
    return -1 
    
def editSculptFrame():
    
    global editState 
    
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)  
    frame = pm.textScrollList("SculptLayers_tsl", q=True, si=True)
    bshps =  pm.getAttr(ssn + '.bshps')
    

    if len(frame )<  1:
        pm.warning("MS Shot-Sculptor: " +"No Frame selected")
        return


    ##set time to the time of the SculptFrame
    time  = str(frame[0]).split('_')[1]       
    
    if  editState:
        pm.button("editSculptFrame_b", e = True, bgc = [0.35, 0.35, 0.35] , l = "Edit Sculpt-Frame" ) 
        
        
        for bshp in bshps:
            pm.sculptTarget(bshp, e=True,t = -1)  # @UndefinedVariable
        
        pm.select(cl=True)
        pm.mel.eval("setToolTo $gSelect;")
        
        editState = False 
        
    else: 
        influence_objs = pm.getAttr(ssn + '.influenceObjs')
        
        pm.currentTime(int (time), e = True)
         
        ##set the sculptTargetMode for all blendshapes
        for bshp in bshps:
            index =getIndexByName (bshp, frame[0])
            pm.sculptTarget(bshp, e=True,t = index)  # @UndefinedVariable
        
        ##set UI functions
        pm.button("editSculptFrame_b", e = True, bgc = [01, 0, 0] , l = "Editing " + frame[0] )
        
        pm.select(influence_objs)   
        pm.mel.eval("SetMeshGrabTool")
        editState = True 
        
def editAnimCurve():
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)  
    frame = pm.textScrollList("SculptLayers_tsl", q=True, si=True)
    
    if len(frame )< 1:
        pm.warning("MS Shot-Sculptor: " +"No Frame selected")
        return

    
    attr = ssn + '.' + frame[0] 
    time  = str(frame[0]).split('_')[1]
    
    pm.select(ssn)
    autoKey(attr, int(time))   

def deleteShotSculptNode():
    global editState 
    
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)
    bshps =  pm.getAttr(ssn + '.bshps')
    
    result = pm.confirmDialog(
                title='Delete Shot Sculpt Group',
                message='Are you sure you want to delete ' +ssn  + "?",
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No')
     
    if result == 'Yes':    
        
        ##exit editmode if enabled
        if editState:
            editSculptFrame()
        
        pm.textFieldGrp("selectedSSNode_tfg", edit = True,text = "No Active Shot-Sculpt group") 
        pm.textScrollList("SculptLayers_tsl",e =True, ra = True)
        pm.delete(ssn, bshps)
    
def deleteShotSculptFrame():
    
    if editState ==True:
        editSculptFrame()   
    
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)
    bshps =  pm.getAttr(ssn + '.bshps')
    frame = pm.textScrollList("SculptLayers_tsl", q=True, si=True)

    result = pm.confirmDialog(
                title='Delete Sculpt-Frame',
                message='Are you sure you want to delete ' + frame[0]  + "?",
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No')
    
    if result == 'Yes':    
        pm.deleteAttr(ssn + '.' + frame[0] )  # @UndefinedVariable
        
        pm.textScrollList("SculptLayers_tsl" , e =True , ri  = str(frame[0]))
                          
        for bshp in bshps:
            ##mel command: blendShapeDeleteTargetGroup + bshp + index
            index  =   getIndexByName(bshp, frame[0])  
            
            #remove the alias
            pm.aliasAttr(bshp + '.' + frame[0], remove = True)  # @UndefinedVariable
            ##delete the target
            pm.removeMultiInstance(bshp + '.weight[' + str(index) + ']', b= True)  # @UndefinedVariable
          
def unloadShotSculptGroup():
    
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)
    if ssn == "No Active Shot-Sculpt group":
        return
    
    pm.textFieldGrp("selectedSSNode_tfg", e =True ,text = "No Active Shot-Sculpt group")
    pm.textScrollList("SculptLayers_tsl", e =True, ra =True)
    
def reloadShotSculptGroup():
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)
    selFrame = pm.textScrollList("SculptLayers_tsl", q = True, sii = True)
    
    pm.select(ssn)
    loadShotSculptNode()
    pm.select(cl = True)
    
    selFrame = pm.textScrollList("SculptLayers_tsl", e = True, sii = selFrame)
    
def toggleEnvelope():
    ssn  =  pm.textFieldGrp("selectedSSNode_tfg", q =True, text = True)
    attr = ssn + ".envelope"
    
    if pm.getAttr(attr) == True:
        pm.setAttr(attr, False)
        pm.headsUpMessage("Shot Sculpt Disabled")       
        
    elif pm.getAttr(attr) == False:
        pm.setAttr(attr, True)
        pm.headsUpMessage("Shot Sculpt Enabled")
            
window_obj = "MS_shotSculptor"
window_label = "MS-Shot-Sculptor--v0.01 "

if pm.window(window_obj, t= window_label, ex = True):
    pm.deleteUI(window_obj)
    
MS_shotSculpt_win = pm.window(window_obj, t = window_label, wh = (230,410) , s=False)

main_frame = pm.frameLayout(lv = False, mw = 10, mh = 10, p = MS_shotSculpt_win)
with main_frame:
    
    nodePanel = pm.frameLayout(l = "Shot Sculpt Node")
    with nodePanel:
        
        with pm.columnLayout():
            pm.button(l = "Create Shot Scupt Group",ann = "Select all mesh objects to influnce ", w = 210, h = 30, c = pm.Callback(createShotSculptNode) ) ##create a ShotSculptNode from selection
            
            with pm.rowLayout(numberOfColumns = 2):  
                pm.textFieldGrp("selectedSSNode_tfg",ann = "Active Shot-Sculpt group",text = "No Active Shot-Sculpt group", editable = False,  w = 175) 
                with pm.popupMenu() :
                    pm.menuItem("Select Shot-Sculpt group",ann = "Select the active Shot-Sculpt group" ,c = "import pymel.core as pm ;pm.select(pm.textFieldGrp('selectedSSNode_tfg', q =True, text = True))" )
                    pm.menuItem("Select Influenced Objects", ann = "Select all objects influenced by the Shot-Sculpt group.",c = "import pymel.core as pm ;ssn = pm.textFieldGrp('selectedSSNode_tfg', q =True, text = True); attr = pm.getAttr(ssn + '.influenceObjs'); pm.select(attr)" )
                    pm.menuItem("Toggle [On/Off]", ann = "Toggle the Shot-Sculpt group on and off", c = pm.Callback(toggleEnvelope))
                 
                pm.button("loadSSNode_b",l = u'\u25c4'  , ann = "Load selected Shot-Sculpt group",w = 30, h =18, c = pm.Callback (loadShotSculptNode))   ## load selected SculptNode as current and update UI
                with pm.popupMenu():
                    pm.menuItem ("Reload", ann = "Reload the Active Shot-Sculpt group" , c = pm.Callback(reloadShotSculptGroup))
                    pm.menuItem ("Unload" ,ann = "Unload the Active Shot-Sculpt group"  , c = pm.Callback(unloadShotSculptGroup)) 
                    pm.menuItem("Delete", ann = "Delete the active Shot-Sculpt group" , c = pm.Callback(deleteShotSculptNode) )
     
                
            pm.textScrollList("SculptLayers_tsl",ann = "Existing Sculpt-Frames",numberOfRows = 8, w = 209)
            with pm.popupMenu() :
                pm.menuItem("Go to Frame", ann = "Go to the Sculpt-Frame" ,c = "import pymel.core as pm ;frame = pm.textScrollList('SculptLayers_tsl', q=True, si=True); pm.currentTime(int(str(frame[0]).split('_')[1]), e=True)")
                pm.menuItem("Edit Sculpt-Frame", ann = "Edit the Sculpt-Frame. (Toggle to exit edit mode)",c = pm.Callback(editSculptFrame))
                pm.menuItem("Edit Anim Curves", ann = "Edit the Animation Curves of the Sculpt-Frame", c = pm.Callback(editAnimCurve))
                pm.menuItem("Delete Sculpt-Frame",ann = "Delete the Sculpt-Frame"  , c = pm.Callback(deleteShotSculptFrame) )
           
    KeyframePanel = pm.frameLayout(l = "Auto Key", )
    with KeyframePanel:
        pm.separator(style = "none")
        with pm.rowLayout(numberOfColumns  =4,  ct4  = ["left", "left", "left", "left" ], co4 = [5, 2,0,2]  ,columnWidth4  = [50,50, 50, 50 ] ):
         
            pm.text("Ease In")
            pm.text("Hold In")
            pm.text("Hold Out")
            pm.text("Ease Out")
            
            
            
            
        arrowUp = u'\u25b2'
        arrowDown = u'\u25bc'
        
        with pm.rowLayout(numberOfColumns  =8,  ct4  = ["left", "left", "left", "left" ], co4 = [5, 0,0,0]  ,columnWidth4  = [50, 50, 50, 50 ] ):
            
            pm.intField ("EaseInIntFeild",ann = "Ease in time (in frames)" ,v= 2, w = 30, h = 30)
            with pm.columnLayout():
                pm.button(arrowUp,ann = "Add Frame" , w = 15 , h = 15, c = pm.Callback (editIntFeild,"EaseInIntFeild",1 ))
                pm.button(arrowDown,ann = "Subtract Frame", w = 15 , h = 15, c = pm.Callback (editIntFeild,"EaseInIntFeild",-1 ))
                
            pm.intField ("HoldInIntFeild", ann = "Hold in time (in frames)" ,v= 0, w = 30, h = 30)
            with pm.columnLayout():
                pm.button(arrowUp,ann = "Add Frame" , w = 15 , h = 15, c = pm.Callback (editIntFeild,"HoldInIntFeild",1 ))
                pm.button(arrowDown,ann = "Subtract Frame", w = 15 , h = 15, c = pm.Callback (editIntFeild,"HoldInIntFeild",-1 ))
                
            pm.intField ("HoldOutIntFeild ", ann = "Hold out time (in frames)" ,v= 0, w = 30, h = 30)
            with pm.columnLayout():
                pm.button(arrowUp,ann = "Add Frame" ,w = 15 , h = 15, c = pm.Callback (editIntFeild,"HoldOutIntFeild",1 ))
                pm.button(arrowDown,ann = "Subtract Frame", w = 15 , h = 15, c = pm.Callback (editIntFeild,"HoldOutIntFeild",-1 ))
                
            pm.intField ("EaseOutIntFeild", ann = "Ease out time (in frames)", v= 2, w = 30, h = 30)
            with pm.columnLayout():
                pm.button(arrowUp, ann = "Add Frame" ,w = 15 , h = 15, c = pm.Callback (editIntFeild,"EaseOutIntFeild",1 ))
                pm.button(arrowDown,ann = "Subtract Frame",w = 15 , h = 15, c = pm.Callback (editIntFeild,"EaseOutIntFeild",-1 ))
            
        with pm.rowLayout(numberOfColumns  =2,  ct2  = ["left", "left"], co2 = [5,0] ,columnWidth2  = [100, 100 ] ):
            
            pm.optionMenu("EaseInTangetType_optmenu", ann = "In Tangent Type", l = "In", w = 90)
            pm.menuItem( l  = "Auto")
            pm.menuItem( l  = "spline")
            pm.menuItem( l  = "linear")
                        
            pm.optionMenu("EaseOutTangetType_optmenu", ann = "Out Tangent Type", l = "Out", w = 100)
            pm.menuItem( l  = "Auto")
            pm.menuItem( l  = "spline")
            pm.menuItem( l  = "linear")
    SculptsPanel = pm.frameLayout(l = "Create and Edit Frames", labelVisible = False )
    with SculptsPanel:
        pm.separator()
        with pm.columnLayout():
           
            pm.button("createSculptFrame_b", ann = "Create a new Sculpt-Frame at the current Time" ,l = "Create Sculpt-Frame", h=40, w = 210, c = pm.Callback(createSculptFrame))
            pm.separator()
            
            with pm.rowLayout(numberOfColumns=2):
                pm.button("editSculptFrame_b",ann = "Edit the selected Sculpt-Frame", l = "Edit Sculpt-Frame", h=20,w = 103, c = pm.Callback(editSculptFrame) )
                pm.button("editCurves_b",ann = "Edit the selected Sculpt-Frame Animation Curves", l = "Edit anim Cruve", h=20,w = 103, c = pm.Callback(editAnimCurve) )
     
pm.showWindow(window_obj)

    
    
    
    
