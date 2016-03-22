################################################################################
"""
aiLightResSetup
Version : v1.0

description: use to setup light image resolution according to input image size
"""
###############################################################################


import sys
sys.path.append('/X/tools/binlinux/oiio/oiio_1.2.0/python')
import OpenImageIO as oiio
import maya.cmds as mc

class aiLightResSetup(object):
    
    def __init__(self):

        self.setImageRes()
    
    def getSkyDomeLgtList(self,*args):
        """ Get all aiSkyDomeLights in the scene """
        lgtList = mc.ls(type='aiSkyDomeLight')
        return lgtList

    def getAreaLgtList(self,*args):
        """ Get all aiAreaLights in the scene """
        lgtList = mc.ls(type='aiAreaLight')
        return lgtList
    
    def imgInfo(self,img):
        """ Returns the image width """
        try:
            read=oiio.ImageInput.open(img)
        except:
            print "Bad image path -- please try again."
            return
        else:
            specs=oiio.ImageSpec(read.spec())
            imageWidth = specs.width
        return imageWidth
        
    def imgPath(self,lgt):
        """ Returns the image path """
        textureFile = mc.listConnections(lgt+'.color')
        if not textureFile:
            filePath = 'None'
        else:
            if mc.objExists(textureFile[0]+'.fileTextureName'):
                filePath = mc.getAttr(textureFile[0]+'.fileTextureName')
            else:
                filePath = 'None'
        return filePath
        
    def setImageRes(self):
        """ Sets image width to resolution """
        skyDomeLgtList = self.getSkyDomeLgtList()
        areaLgtList = self.getAreaLgtList()
        print ''
        print '-------------------------------------------------'
        for lgt in skyDomeLgtList:
            lgtName = mc.listRelatives(lgt,p=True)
            img = self.imgPath(lgt)
            if img == 'None':
                print '# '+ lgtName[0] + '  ===> no file image attached'
            else:
                xres = self.imgInfo(str(img))
                mc.setAttr(lgt+'.resolution',int(xres))
                print '# ' + lgtName[0] + ' ===> set resolution to [ ' + str(xres) + ' ]'
        for lgt in areaLgtList:
            lgtName = mc.listRelatives(lgt,p=True)
            img = self.imgPath(lgt)
            if img == 'None':
                print '# '+ lgtName[0] + '  ===> no file image attached'
            else:
                xres = self.imgInfo(str(img))
                mc.setAttr(lgt+'.aiResolution',int(xres))
                print '# ' + lgtName[0] + ' ===> set resolution to [ ' + str(xres) + ' ]'        

        print '-------------------------------------------------'
        print ''

aiLightResSetup = aiLightResSetup()
