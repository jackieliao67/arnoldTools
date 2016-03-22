##############################################
"""
lightGroupEditor
Version: v1.0

Description: earlier version of mtoaSetManager
"""
##############################################


import maya.cmds as mc
import pymel.core as pm

class lightGroupEditor(object):

    def __init__(self):
        # define number of light groups
        self.lightGroupAmount = 20
        # define light group colors
        self.colorList = [(.5,.1,.1),(.8,.3,.1),(.9,.7,.4),(.2,.6,.2),(.2,.5,.9),(.1,.1,.5),(.5,.5,.9),(.3,.1,.4),(.7,.5,.5),(.4,.8,.3)]
        # build UI
        self.buildUI()

    def buildUI(self,*args):
        sceneLights = self.getSceneLights()
        # create window
        if mc.window("lightGroupEditor",ex=True):
            mc.deleteUI("lightGroupEditor")
        mc.window("lightGroupEditor",w=270,h=100,t="lightGroupEditor",sizeable=True,titleBar=True)
        mc.columnLayout(cal = 'center')
        # create upper buttons
        mc.rowLayout(nc = 3, cw3 = (90,90,90), adjustableColumn = 3, cal = [(1,'center'),(2,'center'),(3,'center')],columnAttach=[(1, 'both', 0), (2, 'both', 0),(3,'both',0)])
        mc.button(l = 'Set All', c = self.setAllButton)
        mc.button(l = 'Clear All', c = self.clearAllButton)
        mc.button(l = 'Refresh', c = self.buildUI)
        mc.setParent('..')
        mc.separator(height = 10, width = 270 )
        mc.rowLayout(nc = 2, cw2 = (30,240), adjustableColumn = 2, cal = [(1,'center'),(2,'left')],columnAttach = [(1,'both',0),(2,'both',0)])
        mc.text(l = '#')
        mc.text(l = ' Light List')
        mc.setParent('..')
        # create center light list
        mc.columnLayout()
        self.buildList()
        mc.setParent('..')
        mc.setParent('..')
        # create lower buttons
        mc.rowLayout(nc = 4, cw4 = (30,105,35,100), adjustableColumn = 4, cal = [(1,'center'),(2,'right'),(3,'center'),(4,'center')],columnAttach=[(1, 'both', 0), (2, 'both', 0),(3,'both',0),(4,'both',0)])
        mc.text('')
        mc.text(l='New Group Number: ')
        mc.intField("editValue", value = 0)
        mc.button(l = 'Set Selected', c =self.editLightGroupsButton)
        mc.setParent('..')
        mc.separator(height = 10, width = 270 )
        mc.button(l = 'Delete Attributes', c =self.deleteAttrButton)
        mc.showWindow()

    def getSceneLights(self):
        # returns a list of lights in the scene
        allLightTypes = pm.listNodeTypes( 'light' )
        scene_lights = []
        for node in pm.ls(dag=True, s=True, l=True):
            if node.nodeType() in allLightTypes:
                scene_lights.append(node)
        return scene_lights

    def buildList(self):
        # separate lights to different groups
        lightGroupList = [[] for x in xrange(self.lightGroupAmount+1)]
        displayList = []
        sceneLights = self.getSceneLights()
        for lgt in sceneLights:
            if lgt.hasAttr("mtoa_constant_lightGroup"):
                groupId = lgt.getAttr("mtoa_constant_lightGroup")
                if groupId > self.lightGroupAmount or groupId < 0:
                    lgt.setAttr('mtoa_constant_lightGroup', 0)
                    lightGroupList[0].append(lgt.name())
                else:
                    lightGroupList[groupId].append(lgt.name())
            else:
                lightGroupList[0].append(lgt.name())
        # build light list and group number
        mc.rowLayout(nc = 2,cw = [(1,30),(2,240)],cal = [(1,'right'),(2,'left')], rat = [(1,'top',0),(2,'top',0)])
        mc.rowColumnLayout(nc = 1, cw = (1,30),cal = (1,'center'))
        # build the light list with the group number > 0 
        for i in range(1,self.lightGroupAmount+1):
            for obj in lightGroupList[i]:
                shortName = mc.listRelatives(obj,p=True)
                longName = mc.listRelatives(obj,p=True,f=True)
                splitVar = len(longName[0].split('|'))
                if splitVar <= 2:
                    mc.text(l=i,bgc = self.colorList[(i-1)-(i/10)*10])
                    displayList.append(shortName[0])
                else :
                    mc.text(l=i,bgc = self.colorList[(i-1)-(i/10)*10])
                    displayList.append(longName[0])
        # build the light list with group number = 0
        for obj in lightGroupList[0]:
            shortName = mc.listRelatives(obj,p=True)
            longName = mc.listRelatives(obj,p=True,f=True)
            splitVar = len(longName[0].split('|'))
            if splitVar <= 2:
                mc.text(l='')
                displayList.append(shortName[0])
            else:
                mc.text(l='')
                displayList.append(longName[0])
        mc.setParent('..')
        mc.textScrollList('mainList', ams = True, w = 240, h = 360, append = displayList)

    def setAllButton(self,*args):
        sceneLights = self.getSceneLights()
        attrValueList = []
        freeNumList = []
        # get the group number which has been using
        for lgt in sceneLights:
            if lgt.hasAttr("mtoa_constant_lightGroup"):
                if lgt.getAttr("mtoa_constant_lightGroup") != 0:
                    attrValue = lgt.getAttr("mtoa_constant_lightGroup")
                    attrValueList.append(attrValue)
        # get the group number which is available to use
        for i in range(1,self.lightGroupAmount+1):
            if i not in attrValueList:
                freeNumList.append(i)
        # set group to undefined lights
        idx = 0
        for lgt in sceneLights:
            if lgt.hasAttr("mtoa_constant_lightGroup"):
                if lgt.getAttr("mtoa_constant_lightGroup") != 0:  
                    pass
                else:
                    if idx < len(freeNumList):
                        lgt.setAttr('mtoa_constant_lightGroup', freeNumList[idx])
                        idx = idx + 1
            else:
                if idx < len(freeNumList):
                    lgt.addAttr('mtoa_constant_lightGroup', attributeType='long', defaultValue=1)
                    lgt.setAttr('mtoa_constant_lightGroup', freeNumList[idx])
                    idx = idx + 1    

        self.buildUI() 

    def clearAllButton(self,*args):
        sceneLights = self.getSceneLights()
        # Set all lights to group 0 
        for lgt in sceneLights:   
            if lgt.hasAttr("mtoa_constant_lightGroup"):
                lgt.setAttr('mtoa_constant_lightGroup', 0)                  

        self.buildUI() 
    
    def deleteAttrButton(self,*args):
        sceneLights = self.getSceneLights()
        # delete Attribute from all lights
        for lgt in sceneLights:
            lightName = mc.listRelatives(lgt.name(),p=True)
            if lgt.hasAttr("mtoa_constant_lightGroup"):
                lgt.deleteAttr('mtoa_constant_lightGroup')  

        self.buildUI() 

    def editLightGroupsButton(self,*args):
        # set new group number to selected lights
        selectedLights = mc.textScrollList('mainList', q = True, si = True, fpn = True)
        newGroupId = mc.intField("editValue", q = True, value = True)
        if selectedLights != None:
            for lgt in selectedLights:
                splitVar = len(lgt.split('|'))
                if splitVar == 1:
                    newLgtName = str('|'+lgt)
                    lgtShape = mc.listRelatives(newLgtName,s=True,f=True)
                    if mc.objExists(lgtShape[0] +".mtoa_constant_lightGroup"):
                        mc.setAttr(lgtShape[0]+'.mtoa_constant_lightGroup', newGroupId)
                    else:
                        mc.addAttr(lgtShape[0],ln = "mtoa_constant_lightGroup",sn = "mtoa_constant_lightGroup",at = "long",dv = 1)
                        mc.setAttr(lgtShape[0]+'.mtoa_constant_lightGroup', newGroupId)
                else:
                    lgtShape = mc.listRelatives(lgt,s=True,f=True)
                    if mc.objExists(lgtShape[0] +".mtoa_constant_lightGroup"):
                        mc.setAttr(lgtShape[0]+'.mtoa_constant_lightGroup', newGroupId)
                    else:
                        mc.addAttr(lgtShape[0],ln = "mtoa_constant_lightGroup",sn = "mtoa_constant_lightGroup",at = "long",dv = 1)
                        mc.setAttr(lgtShape[0]+'.mtoa_constant_lightGroup', newGroupId)              
            self.buildUI()


lightGroupEditor=lightGroupEditor()
