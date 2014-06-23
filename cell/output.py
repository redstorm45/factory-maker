import pygame
from pygame.locals import *
import cell.cell
import util
import math

colorBase = (175,175,175)

class Output(cell.cell.Cell):
    def __init__(self,infos):
        self.orient = int(infos[0])
        self.color = util.getColorFromStr(infos[1])
        self.id = int(infos[2])
        
        self.acceptAny = ( infos[1] == "any" )

    def makeSurf(self,size):#size is the size of the base square
        outSize = size * 5/4
        holeStart = size/4
        holeEnd = size/4 * 3

        self.offset = ( -size/4 , -size/4 )

        self.baseSurf = pygame.Surface( (outSize,outSize) , SRCALPHA)
        self.staticSurf = None
        pointsTop = [ #borders around
                      (0,0) ,
                      (size,0) ,
                      (size,size),
                      (0,size) ,
                      (0,0) ,
                      #hole in the middle
                      (holeStart,holeStart),
                      (holeStart,holeEnd),
                      (holeEnd,holeEnd),
                      (holeEnd,holeStart),
                      (holeStart,holeStart)]
        pointsRight = [ (size,0) ,
                        (outSize,outSize-size) ,
                        (outSize,outSize),
                        (size,size) ]
        pointsFront = [ (0,size) ,
                        (outSize-size,outSize) ,
                        (outSize,outSize),
                        (size,size) ]
        pointsHoleLeft = [ (holeStart,holeStart) ,
                           (holeEnd,holeEnd) ,
                           (holeStart,holeEnd) ]
        pointsHoleTop = [ (holeStart,holeStart) ,
                           (holeEnd,holeEnd) ,
                           (holeEnd,holeStart) ]
        
        baseArrowPoints = [ (size/4+size/16,0),
                            (size/2-size/16,size/4),
                            (size/2-size/16,-size/4)]
        pointsArrow = util.translatePoints( util.rotatePoints( baseArrowPoints , self.orient*math.pi/2 ) , (size/2,size/2) )

        #shadow inside the hole
        pygame.draw.polygon( self.baseSurf , util.multColor(colorBase,0.8) , pointsHoleLeft )
        pygame.draw.polygon( self.baseSurf , util.multColor(colorBase,0.5) , pointsHoleTop )
        #draw the basic shape
        pygame.draw.polygon( self.baseSurf , colorBase , pointsTop )
        pygame.draw.polygon( self.baseSurf , util.multColor(colorBase,0.8) , pointsRight )
        pygame.draw.polygon( self.baseSurf , util.multColor(colorBase,0.5) , pointsFront )
        #draw inputting arrow
        if self.orient == -1:
            for i in range(4):
                pointsArrow = util.translatePoints( util.rotatePoints( baseArrowPoints , i*math.pi/2 ) , (size/2,size/2) )
                pygame.draw.polygon( self.baseSurf , util.multColor(colorBase,0.5) , pointsArrow )
        pygame.draw.polygon( self.baseSurf , util.multColor(colorBase,0.5) , pointsArrow )

    def draw(self,window,pos):
        window.blit( self.baseSurf , pos )

    def initAnim(self):
        self.iterAnim = 0
        self.outputtingBox = None

    def updateAnim(self):
        if self.iterAnim>0:
            self.iterAnim -= 1

    def makeAnimSurf(self,size):
        if self.outputtingBox and self.iterAnim>0:
            animSize = size * 3/4
            animLength = size * 1/2 - self.outputtingBox.offset/3
            animPos = animSize - animLength * self.iterAnim/50
            self.animSurf = pygame.Surface( (animSize,animSize) ,SRCALPHA)
            self.animSurf.blit( self.outputtingBox.surf , ( animPos,animPos) )
        else:
            self.animSurf = None

    def takeBox(self,b):
        self.iterAnim = 50
        self.outputtingBox = b













    
