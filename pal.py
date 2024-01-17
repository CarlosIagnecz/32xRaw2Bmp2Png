# import required libraries 
import numpy as np 
from PIL import Image as img
import sys
from tkinter import *

#Convert .raw.pal to image
def Pal2Png(hexval,size):
    hexstring = str(hexval)

    #Split every number
    hexstring = [hexstring [i:i+2] for i in range(0, len(hexstring), 2)]
    rawValues = [int(i,16) for i in hexstring]

    pixelSep = []
    for i in range(int(len(rawValues)/3)):
        app = [rawValues[i*3],
            rawValues[i*3+1],
            rawValues[i*3+2]]
        pixelSep.append(app)

    #Reshape Manually
    rowSep = []
    for i in range(int(len(pixelSep)/size[0])):
        app = [pixelSep[(i*size[0])-n] for n in range(size[0])]
        rowSep.append(app)
    return rowSep,pixelSep

#Extract Pallete from image
