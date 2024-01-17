# import required libraries 
import numpy as np 
from PIL import Image as img, ImageTk
import sys
from tkinter import *

#import scripts
from pal import *
from raw import *

# sega 32x mode 1 resolution (NTSC)
palsize = [16,16]
individual = True

def resetWH():
    global widthInp
    global heightInp
    widthInp.delete('0.0', END)
    heightInp.delete('0.0', END)
    widthInp.insert("0.0","320")
    heightInp.insert("0.0","224")

def Rename():
    global directoryraw
    global directorypal
    global directoryinp
    global renButton
    global individual
    
    individual = not individual
    if individual:
        directorypal.configure(state=NORMAL)
        directoryraw.configure(state=NORMAL)
        directorypal.delete('0.0', END)
        directoryraw.delete('0.0', END)
        renButton.config(text = "Get directory from '.png'") 
    else:
        directorypal.delete('0.0', END)
        directoryraw.delete('0.0', END)
        directorypal.insert("0.0","Copying from '.png'")
        directoryraw.insert("0.0","Copying from '.png'")
        directorypal.configure(state=DISABLED)
        directoryraw.configure(state=DISABLED)
        
        renButton.config(text = "Get directory from individual") 
def Decode():
    global palsize
    global txtoutputlbl
    global individual

    global directoryraw
    global directorypal
    global directoryinp
    global imgDisp

    global widthInp
    global heightInp
    try:
        rawsize = [round(int(widthInp.get(1.0, "end-1c"))),round(int(heightInp.get(1.0, "end-1c")))]
    except:
        txtoutputlbl.config(text = "Text Output:\n Invalid size (not int)") 
        return None
    if rawsize[0] < 1 or rawsize[1] < 1:
        txtoutputlbl.config(text = "Text Output:\n Invalid size (too small)") 
        return None
    if rawsize[0] > 320 or rawsize[1] > 240:
        txtoutputlbl.config(text = "Text Output:\n Invalid size (too big)") 
        return None
    inpTxt = directoryinp.get(1.0, "end-1c")
    if individual:
        palfile = directorypal.get(1.0, "end-1c")
        rawfile = directoryraw.get(1.0, "end-1c")
    else:
        cutInp = inpTxt.split(".")[0]
        palfile = f"{cutInp}.raw.pal"
        rawfile = f"{cutInp}.raw"
    # open pallete file
    try:
        with open(palfile, 'rb') as f:
            hexval = f.read().hex()
    except:
        txtoutputlbl.config(text = "Text Output:\n Invalid directory for pallete") 
        return None
    
    rowSep,palVal = Pal2Png(hexval,palsize)

    amm = len(rowSep)*len(rowSep[0])
    palexpected = palsize[0]*palsize[1]
    if amm == palexpected:
        status = "OK"
    elif amm < palexpected:
        status = f"Under limit"
    elif amm > palexpected:
        status = f"Exceeded pallete limit"

    txtoutputlbl.config(text = f"Text Output:\n Expected Pallete Size: {palexpected}\n----------------------------------------\nTotal Palletes: {amm}\n----------------------------------------\nPalletes per row: {len(rowSep[0])}x{len(rowSep)}\n----------------------------------------\nPallete Status: {status}\n----------------------------------------\n") 

    # translated pallete image
    image_translated = np.array(rowSep, dtype=np.uint8)

    # save pallete image
    palimage = img.fromarray(image_translated)
    palimage.save('pallete_export_from_pal.png')

    #Convert Pallete for usage in bmp
    palimage.getpalette()

    # open raw file
    try:
        with open(rawfile, 'rb') as f:
            hexval = f.read().hex()
    except:
        txtoutputlbl['text'] += "Invalid directory for raw image"
        return None

    rawPng = Raw2Bmp2Png(hexval,rawsize,palVal)

    rawamm = len(rawPng)*len(rawPng[0])
    imgexpected = rawsize[0]*rawsize[1]
    if rawamm == imgexpected:
        rawstatus = "OK"
    elif rawamm < imgexpected:
        rawstatus = f"Under limit by {imgexpected-rawamm} pixels!"
    elif rawamm > imgexpected:
       rawstatus = f"Exceeded image size limit by {rawamm-imgexpected} pixels!"

    txtoutputlbl['text'] += f"Expected Raw Image Size: {imgexpected}\n----------------------------------------\nTotal Size: {rawamm} pixels\n----------------------------------------\nRaw Resolution: {len(rawPng[0])}x{len(rawPng)}\n----------------------------------------\nImage Status: {rawstatus}\n----------------------------------------\n"

    # translated raw image
    image_translated = np.array(rawPng, dtype=np.uint8)

    # save raw image
    rawimage = img.fromarray(image_translated)
    try:
        rawimage.save(inpTxt)
        txtoutputlbl['text'] += f"Succesfully saved '.png' {inpTxt}\n----------------------------------------\n"
    except:
        txtoutputlbl['text'] += f"Failed to save '.png' {inpTxt}, make sure it's in a valid directory\n----------------------------------------\n"
    imgforDisp = ImageTk.PhotoImage(rawimage)
    imgDisp.config(image=imgforDisp)
    imgDisp.image=imgforDisp

def Encode():
    global imgDisp

    global palsize
    global txtoutputlbl

    global directoryraw
    global directorypal
    global directoryinp
    global widthInp
    global heightInp
    try:
        rawsize = [round(int(widthInp.get(1.0, "end-1c"))),round(int(heightInp.get(1.0, "end-1c")))]
    except:
        txtoutputlbl.config(text = "Text Output:\n Invalid size (not int)") 
        return None
    if rawsize[0] < 1 or rawsize[1] < 1:
        txtoutputlbl.config(text = "Text Output:\n Invalid size (too small)") 
        return None
    if rawsize[0] > 320 or rawsize[1] > 240:
        txtoutputlbl.config(text = "Text Output:\n Invalid size (too big)") 
        return None
    
    dirInp = directoryinp.get(1.0, "end-1c")
    #Pallete and Raw Files
    if individual:
        palfile = directorypal.get(1.0, "end-1c")
        rawfile = directoryraw.get(1.0, "end-1c")
    else:
        cutInp = dirInp.split(".")[0]
        palfile = f"{cutInp}.raw.pal"
        rawfile = f"{cutInp}.raw"

    
    try:
        pngImg = img.open(dirInp)
    except:
        txtoutputlbl.config(text = f"Text Output:\n Invalid directory for '.png': {dirInp}") 
        return None
    imgforDisp = ImageTk.PhotoImage(pngImg)
    imgDisp.config(image=imgforDisp)
    imgDisp.image=imgforDisp
    mode = pngImg.mode #P == Pallete, RGB = True Color
    if not (mode == "P" or mode == "RGB" or mode == "RGBA"):
        txtoutputlbl.config(text = f"Text Output:\n Invalid mode for Image (P/RGB/RGBA only!): {mode}") 
        return None
    if mode != "P":
        pngImg = pngImg.quantize(colors=256, method=2)
    #Pallete
    imgPal = pngImg.getpalette()
    pixPal = []
    for i in range(int(len(imgPal)/3)):
        app = [imgPal[i*3],
            imgPal[i*3+1],
            imgPal[i*3+2]]
        pixPal.append(app)

    #Reshape Manually
    rowPal = []
    for i in range(1,int(len(pixPal)/palsize[0])+1):
        app = [pixPal[(i*palsize[0])-n-1] for n in range(palsize[0])]
        rowPal.append(app)

    palAmm = len(pixPal)
    palexpected = palsize[0]*palsize[1]
    if palAmm == palexpected:
        palStatus = "OK"
    elif palAmm < palexpected:
        palStatus = f"Under limit"
    elif palAmm > palexpected:
        palStatus = f"Exceeded pallete limit"

    txtoutputlbl.config(text = f"Text Output:\nExpected Pallete Size: {palexpected}\n----------------------------------------\nTotal Colors: {palAmm} pixels\n----------------------------------------\nPallete Rows: {len(rowPal[0])}x{len(rowPal)}\n----------------------------------------\nPallete Status: {palStatus}\n----------------------------------------\n")
        
    # translated pallete image
    pal_translate = np.array(rowPal, dtype=np.uint8)

    # save pallete image
    palimage = img.fromarray(pal_translate)
    palimage.save('pallete_export_from_png.png')

    #BMP to RAW
    np_img = np.array(pngImg)

    rawhex,palhex = Bmp2Raw(np_img,pixPal)
    txtoutputlbl['text'] += f"Raw Byte Size: {len(rawhex)}\n----------------------------------------\nPal Byte Size: {len(palhex)}\n----------------------------------------\n"

    #Write to file
    try:
        with open(rawfile, "wb") as bin_raw:
            bin_raw.write(rawhex)
            txtoutputlbl['text'] += f"Succesfully saved '.raw' {rawfile}\n----------------------------------------\n"
    except:
        txtoutputlbl['text'] += f"Failed to save '.raw' {rawfile}, make sure it's in a valid directory\n----------------------------------------\n"
    
    try:
        with open(palfile, "wb") as bin_pal:
            bin_pal.write(palhex)
            txtoutputlbl['text'] += f"Succesfully saved '.raw.pal' {palfile}\n----------------------------------------\n"
    except:
        txtoutputlbl['text'] += f"Failed to save '.raw.pal' {palfile}, make sure it's in a valid directory\n----------------------------------------\n"
    
#Tkinter Window
surf = Tk()
surf.title("32xRaw2Bmp2Png") 
surf.geometry('640x896')

#Labels
info = Label(surf, text = "Made by Carlos Iagnecz in 2024 (v1.0)")
rflbl = Label(surf, text = "'.raw' file directory:")
pflbl = Label(surf, text = "'.raw.pal' file directory:")
iflbl = Label(surf, text = "'.png' file directory:")
txtoutputlbl = Label(surf, text = "Text Output:")
imgoutputlbl = Label(surf, text = "Image Output:")
# Directory Inputs
directoryraw = Text(surf, height = 1, width = 25)

directorypal = Text(surf, height = 1, width = 25)

directoryinp = Text(surf, height = 1, width = 25)

#Width Height Stuff
wlbl = Label(surf, text = "Width:")
widthInp = Text(surf, height = 1, width = 3)
hlbl = Label(surf, text = "Height:")
heightInp = Text(surf, height = 1, width = 3)

resetWH()

# Buttons
encButton = Button(surf, text = "Encode",  command = Encode)
decButton = Button(surf, text = "Decode",  command = Decode)
renButton = Button(surf, text = "Get directory from '.png'",  command = Rename)
resButton = Button(surf, text = "Reset Size",  command = resetWH)

#Image
imgDispFrame = Frame(surf, width=320, height=224)
imgDisp = Label(imgDispFrame)

#Package Window
info.pack(anchor=NW)
wlbl.pack(anchor=NW)
widthInp.pack(anchor=NW)
hlbl.pack(anchor=NW)
heightInp.pack(anchor=NW)
resButton.pack(anchor=NW)
rflbl.pack()
directoryraw.pack()
pflbl.pack()
directorypal.pack()
decButton.pack()
iflbl.pack()
directoryinp.pack()
encButton.pack()
renButton.pack()
imgoutputlbl.pack()
imgDispFrame.pack()
imgDisp.pack()
txtoutputlbl.pack()

