#######################################################################
# Tools for Connecting Custom AOVs to defaultArnoldRenderOptions Node #
#                                                                     #
# Version : v0.1                                                      #
#                                                                     #
#######################################################################

import maya.cmds as mc

def getAovList():
    allAovs = mc.ls(type='aiAOV')
    aovList = []
    for aov in allAovs:
        connections = mc.listConnections(aov+'.message', d = True)
        if connections is not None:
            if "defaultArnoldRenderOptions" not in connections:
                aovList.append(aov)
    aovList.sort()     
    return aovList

def getAovListNum():
    for i in range(0,100):
        aovListConnections = mc.listConnections('defaultArnoldRenderOptions.aovList['+str(i)+']',c=True)
        if aovListConnections is not None:
            pass
        else:
            return i
            break
            
def connectAov():
    aovList = getAovList()
    print '====================================='
    print 'Custom AOVs Created:'
    print ''
    for aov in aovList:
        aovListNum = getAovListNum()
        mc.connectAttr(aov+'.message','defaultArnoldRenderOptions.aovList[' + str(aovListNum) + ']', f = True)
        print aov
    print ''
    print '====================================='
        
connectAov() 
