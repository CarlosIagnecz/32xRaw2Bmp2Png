# import required libraries 
import numpy as np 
from PIL import Image as img
import sys
from tkinter import *

def Raw2Bmp2Png(hexval,size,pal):
    hexstring = str(hexval)

    #Split every number
    hexstring = [hexstring [i:i+2] for i in range(0, len(hexstring), 2)]
    rawValues = [int(i,16) for i in hexstring]

    #Atribute from pallete
    pixelSep = []
    for i in range(int(len(rawValues))):
        pixelSep.append(pal[rawValues[i]])

    #Reshape Manually
    rowSep = []
    for i in range(1,int(len(pixelSep)/size[0])+1):
        app = [pixelSep[(i*size[0])-n-1] for n in range(size[0])]
        rowSep.append(app)
    return rowSep
def Bmp2Raw(img,pal):
    hexstrraw = ""
    for i in range(len(img)):
        for n in range(len(img[i])):
            hexstrraw = f"{hexstrraw}{img[i][n]:02x}"
    hexraw = bytes.fromhex(hexstrraw)
    hexstrpal = ""
    for i in range(len(pal)):
        for n in range(len(pal[i])):
            hexstrpal = f"{hexstrpal}{pal[i][n]:02x}"
    hexpal = bytes.fromhex(hexstrpal)
    return hexraw,hexpal
