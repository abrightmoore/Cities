# @abrightmoore - generate a bounds limited scattering of rectangles. Use for generating plots of neighbourhoods in cities.
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
import os
import time
from random import randint, random, Random
import io
import sys
from io import BytesIO

from PIL import Image, ImageDraw
import pygame, sys
from pygame.locals import *

DEBUGMAX = False # Disable
DEBUGLOGMETHODCALLS = False
DEBUGLOGMETHODCALLSNESTED = False

GAMENAME = "AJB Plot Caster"

pygame.init()

class Rectangle:
        COL = (255,192,160,255)
        COLCOL = (255,0,0,255)
        
        def __init__(self,label,size,pos,col):
                self.label = label
                self.size = size
                self.pos = pos
                self.col = col
 
        def getPoints(self):
                minx, miny = self.pos
                w, h = self.size
                
                return (minx,miny,minx+w,miny+h)

        def setPos(self,pos):
                self.pos = pos

        def getColour(self):
                return self.col

        def setColour(self,col):
                self.col = col

def doCollisionShift(R,radius):
        minx = 9999999
        miny = minx
        maxx = -9999999
        maxy = maxx
        r2 = radius**2
        collisions = 0
        i = 0 # randint(0,len(R)-1)
        while i < len(R): # and collisions < 100:
                for j in xrange(0,len(R)): # O(n2), not great...
                        if i != j: # Suppress collision with self
                                ri = R[i]
                                rj = R[j]

                                (xi,yi,mxi,myi) = ri.getPoints()
                                (xj,yj,mxj,myj) = rj.getPoints()

                                if xi < minx:
                                        minx = xi
                                if mxi > maxx:
                                        maxx = mxi
                                if yi < miny:
                                        miny = yi
                                if myi > maxy:
                                        maxy = myi

                                # Check for overlap

                                movex = 0
                                movey = 0
                                strategy = randint(0,3)

                                dx = xj - xi
                                dmx = mxj - mxi
                                dy = yj - yi
                                dmy = myj - myi

                                if strategy == 0 and xj <= mxi and yj <= myi and xj >= xi and yj >= yi: # Bottom left is within collision area
                                        if randint(0,1) == 0 and xj >= xi and xj <= mxi:
                                                movex += mxi-xj+1
                                        elif yj >= yi and yj <= myi:
                                                movey += myi-yj+1
                                        # print strategy
                                if strategy == 1 and mxj <= mxi and yj <= myi and mxj >= xi and yj >= yi: # Bottom right is within collision area
                                        if randint(0,1) == 0 and mxj >= xi and mxj <= mxi:
                                                movex += mxi-mxj+1
                                        elif yj >= yi and yj <= myi:
                                                movey += myi-yj+1
                                        # print strategy
                                if strategy == 2 and mxj <= mxi and myj <= myi and mxj >= xi and myj >= yi: # Top right is within collision area
                                        if randint(0,1) == 0 and mxj >= xi and mxj <= mxi:
                                                movex += mxi-mxj+1
                                        elif myj >= yi and myj <= myi:
                                                movey += myi-myj+1
                                        # print strategy
                                if strategy == 3 and xj <= mxi and myj <= myi and xj >= xi and myj >= yi: # Top left is within collision area
                                        if randint(0,1) == 0 and xj >= xi and xj <= mxi:
                                                movex += mxi-xj+1
                                        elif myj >= yi and myj <= myi:
                                                movey += myi-myj+1
                                        # print strategy
                                if xj >= xi and xj <= mxi and mxj >= xi and mxj <= mxi and yj <= yi and myj >= myi: # Intersecting
                                        if randint(0,1) ==0:
                                                movex += mxi-xj
                                        else:
                                                movey += myj-yi
                                
                                # either move the j'th element right or the i'th one left
                                if movex != 0 or movey != 0:
                                        # print movex,movey
                                        
                                        if randint(0,1) == 0:
                                                px = mxj+movex
                                                py = myj+movey
                                                d = px**2+py**2
                                                if d <= r2:                                                        
                                                        px = xj+movex
                                                        py = myj+movey
                                                        d = px**2+py**2
                                                        if d <= r2:                                                        
                                                                px = mxj+movex
                                                                py = yj+movey
                                                                d = px**2+py**2
                                                                if d <= r2:                                                        
                                                                        px = xj+movex
                                                                        py = yj+movey
                                                                        d = px**2+py**2
                                                                        if d <= r2:
                                                                                rj.setPos((px,py))
                                                                                collisions += 1
                                                rj.setColour(Rectangle.COLCOL)
                                        else:
                                                px = mxj-movex
                                                py = myj-movey
                                                d = px**2+py**2
                                                if d <= r2:                                                        
                                                        px = xi-movex
                                                        py = myi-movey
                                                        d = px**2+py**2
                                                        if d <= r2:
                                                                px = mxi-movex
                                                                py = yi-movey
                                                                d = px**2+py**2
                                                                if d <= r2:
                                                                        px = xi-movex
                                                                        py = yi-movey
                                                                        d = px**2+py**2
                                                                        if d <= r2:
                                                                                ri.setPos((px,py))
                                                                                collisions += 1
                                                ri.setColour(Rectangle.COLCOL)
                i += 1
        return (minx,miny,maxx,maxy) # Rendering hint                                        

def mainLoop():
        # Create a bunch of rectangles
        RADIUS = 300
        MAXRECT = int(RADIUS*1.5)
        COL = (255,192,160,255)
        R = []
        D1 = 6
        D2 = 11
        for i in xrange(0,MAXRECT):
                choice = randint(0,2)
                r = None
                if True: # choice == 0:
                        r = Rectangle("Building"+str(i+1), (randint(D1,D2),randint(D1,D2)), (0,0),Rectangle.COL) 
#                elif choice == 1:
#                        r = Rectangle("Building"+str(i+1), (D1,D2), (0,0),Rectangle.COL)
#                else:
#                        r = Rectangle("Building"+str(i+1), (D2,D2), (0,0),Rectangle.COL)
                R.append(r)

        COL_CANVAS =(0,0,0,255)
	img = pygame.image.load('input.png')
	backgroundimage = img
	displayWidth = img.get_width()
	displayHeight = img.get_height()
	surface = pygame.display.set_mode((displayWidth, displayHeight)) # A copy of the source image in size
	surface.fill(COL_CANVAS) # Parchment colour to the canvas
	pygame.display.set_caption('Plot Caster')
        ox = displayWidth>>1
        oy = displayHeight>>1
	
        FPS = 60
	fpsClock = pygame.time.Clock()
	fpsClock.tick(FPS)


        ITERLIMIT = 10000
        iterationCount = 0
        while True and iterationCount < ITERLIMIT:
                iterationCount = iterationCount +1
                # Check for collisions and move colliding rectangles apart
                surface.blit(backgroundimage,[0,0])
                pixels = pygame.PixelArray(surface)
                (minx,miny,maxx,maxy) = doCollisionShift(R,RADIUS)
#                print (minx,miny,maxx,maxy)
 
                scalex = float(displayWidth)/(maxx-minx)
                scaley = float(displayHeight)/(maxy-miny)
#                scalex = 1.0
#                scaley = 1.0
                # print scalex,scaley
                ang = pi/360*2
                for i in xrange(0,360):
                        
                        x = scalex*cos(ang*i)*float(RADIUS)+ox
                        y = scaley*sin(ang*i)*float(RADIUS)+oy
                        x = int(x)
                        y = int(y)
 #                       print x,y
                        if x >=0 and x < displayWidth and y >= 0 and y < displayHeight:                                        
                                pixels[x][y] = (255,255,255,255)

                # Draw all the boxes, around the display centre
 
		for event in pygame.event.get():
			if event.type == QUIT:
				print "Shutting down."
				pygame.quit()
				sys.exit()	

 		for r in R:
                        COL = r.getColour()
                        (x,y,mx,my) = r.getPoints()
 #                       (x,y,mx,my) = (x+ox,y+oy,mx+ox,my+oy)
                        dx = scalex*(maxx-minx)/2
                        dy = scaley*(maxy-miny)/2
                        x = scalex*(x)
                        y = scaley*(y)
                        mx = scalex*(mx)
                        my = scaley*(my)
                        x = int(x)+ox
                        y = int(y)+oy
                        mx = int(mx)+ox
                        my = int(my)+oy
                        
                        if y >= 0 and y < displayHeight:
                                for i in xrange(x,mx+1):
                                        if i >= 0 and i < displayWidth:
                                                pixels[i][y] = COL
                        if my >= 0 and my < displayHeight:
                                for i in xrange(x,mx+1):
                                        if i >= 0 and i < displayWidth:
                                                pixels[i][my] = COL
                        if x >= 0 and x < displayWidth:
                                for i in xrange(y,my+1):
                                        if i >=0 and i < displayHeight:
                                                pixels[x][i] = COL
                        if mx >= 0 and mx < displayWidth:
                                for i in xrange(y,my+1):
                                        if i >=0 and i < displayHeight:
                                                pixels[mx][i] = COL
                        r.setColour(Rectangle.COL)
                del pixels
                pygame.display.update()

                

        # Rinse and repeat until no more collisions or the number of iterations exceeds a limit.


##################

mainLoop()
