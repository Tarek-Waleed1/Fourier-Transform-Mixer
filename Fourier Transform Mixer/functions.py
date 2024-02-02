from PyQt5 import QtGui, QtCore, QtWidgets
import csv
from PyQt5.QtWidgets import QFileDialog, QColorDialog,QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import numpy as np
import pandas as pd
import random
import os
from PIL import Image
from functools import partial
from random import randint
from scipy.signal import resample
from PyQt5.QtGui import QPixmap,QImage
from classes import image
import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



arrayofimages=[image(),image(),image(),image()]
arrayofoutputs=[image(),image()]
usebright=0
isouter=0

def browseall4(self,Imagearray,grapharray,drawtypearray):
    for i in range(4):
       browse(self,Imagearray,grapharray,drawtypearray,i)
#
#
#
#
#
def browse(self,labeltobeimage,graph,drawtype,indexofimage):
    global arrayofimages
    fname,_=QFileDialog.getOpenFileName(self, "open image","C:","All files (*);;PNG Files (*.png) ")
    if fname:
        image= Image.open(fname)
        image=image.convert("L")
        new_image=image.resize((200,200))
        new_image.save(f"Stuffforprogramtowork/{indexofimage}/input.jpg")
        image = cv2.imread(f"Stuffforprogramtowork/{indexofimage}/input.jpg",cv2.IMREAD_GRAYSCALE)
        height, width= image.shape
        arrayofimages[indexofimage].imagedata=image
        arrayofimages[indexofimage].height=height
        arrayofimages[indexofimage].width=width
        arrayofimages[indexofimage].dtype=image.dtype
        arrayofimages[indexofimage].readydata()
        qImg = QImage(image.data, width, height,width,QImage.Format_Grayscale8)
        pixmap=QPixmap.fromImage(qImg)
        labeltobeimage[indexofimage].setPixmap(pixmap)
        changetype(drawtype,graph,indexofimage)

    else:
        return




def handle_contrast_and_brightness(event, label,index,In):
    global arrayofimages
    global arrayofoutputs
    global usebright
    if event.buttons() == Qt.LeftButton:
        delta_x = event.pos().x() - 0
        delta_y = event.pos().y() - 0
        # Adjust the factor based on your needs
        contrast_factor = delta_y / 100.0
        brightness_factor = delta_x / 100.0

        contrast_factor = max(0.0, min(2.0, contrast_factor))
        brightness_factor = max(0.0, min(2.0, brightness_factor))  # Adjusted range for brightness
        brightness_factor*=20
        usebright = 1
        label.start_pos = event.pos()
        if In:
            shape=[arrayofimages[index].height,arrayofimages[index].width]
            image2 = cv2.addWeighted(arrayofimages[index].imagedata, contrast_factor, np.zeros(shape, arrayofimages[index].dtype), 0, brightness_factor)
            cv2.imwrite(f"Stuffforprogramtowork/{index}/inputBr.jpg", image2)
            label.setPixmap(QPixmap(f"Stuffforprogramtowork/{index}/inputBr.jpg"))
        else:
            shape = [arrayofoutputs[index].height, arrayofoutputs[index].width]
            image2 = cv2.addWeighted(arrayofoutputs[index].imagedata, contrast_factor,
                                     np.zeros(shape, arrayofoutputs[index].dtype), 0, brightness_factor)
            cv2.imwrite(f"Stuffforprogramtowork/out/{index}Br.jpg", image2)
            label.setPixmap(QPixmap(f"Stuffforprogramtowork/out/{index}Br.jpg"))

def resetContrastBrightness(Imagearray,outputImage1,outputImage2):
    global arrayofoutputs
    global usebright
    usebright=0
    for i in range(4):
        if not len(arrayofimages[i].Mag)==0:
            Imagearray[i].setPixmap(QPixmap(f"Stuffforprogramtowork/{i}/input.jpg"))
    if not len(arrayofoutputs[0].Mag)==0:
        outputImage1.setPixmap(QPixmap(f"Stuffforprogramtowork/out/{0}.jpg"))
    if not len(arrayofoutputs[1].Mag)==0:
        outputImage2.setPixmap(QPixmap(f"Stuffforprogramtowork/out/{1}.jpg"))






def changetype(drawtype,graph,index):
    global arrayofimages
    if drawtype[index].currentText()=="Magnitude":
        pixmap=QPixmap.fromImage(arrayofimages[index].magimage)
        graph[index].setPixmap(pixmap)
    elif drawtype[index].currentText()=="Phase":
        pixmap=QPixmap.fromImage(arrayofimages[index].phaseimage)
        graph[index].setPixmap(pixmap)
    elif drawtype[index].currentText()=="Real":
        pixmap=QPixmap.fromImage(arrayofimages[index].realcompimage)
        graph[index].setPixmap(pixmap)
    elif drawtype[index].currentText()=="Imaginary":
        pixmap=QPixmap.fromImage(arrayofimages[index].imagcompimage)
        graph[index].setPixmap(pixmap)

def sendToOutput(self,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2,Imageindex):
    global arrayofimages
    global arrayofoutputs
    readydataforoutput(innerregion, regionpercent)

    arrayofoutputs[Imageindex].emptydata()
    for i in range(4):
        if len(arrayofimages[i].Mag)==0:
            arrayofoutputs[Imageindex].OgMagnitudes.append(0)
            arrayofoutputs[Imageindex].OgPhaseshift.append(0)
            arrayofoutputs[Imageindex].Ogrealcomp.append(0)
            arrayofoutputs[Imageindex].Ogimagcomp.append(0)
        else:
            arrayofoutputs[Imageindex].OgMagnitudes.append(arrayofimages[i].constraintmag.copy())
            arrayofoutputs[Imageindex].OgPhaseshift.append(arrayofimages[i].constraintphase.copy())
            arrayofoutputs[Imageindex].Ogrealcomp.append(arrayofimages[i].constraintreal.copy())
            arrayofoutputs[Imageindex].Ogimagcomp.append(arrayofimages[i].constraintimaginary.copy())



    UpdateOutput(self,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2,Imageindex)






def UpdateOutput(self,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2,indexImage):
    global arrayofimages
    global arrayofoutputs
    global isouter
    if len(arrayofoutputs[indexImage].OgMagnitudes)==0:
        return


    magtotal=0
    phasetotal=0
    realtotal=0
    imagetotal=0
    counter=0

    for i in range(4):
        if magphase.isChecked():
            if not len(arrayofimages[i].Mag)==0:
                magtotal += arrayofoutputs[indexImage].OgMagnitudes[i]*arrayofcouplesliders[i][0].value()/1000
                phasetotal+=arrayofoutputs[indexImage].OgPhaseshift[i]*arrayofcouplesliders[i][1].value()/1000
                realtotal+=arrayofoutputs[indexImage].Ogrealcomp[i]
                imagetotal+=arrayofoutputs[indexImage].Ogimagcomp[i]
                counter+=1
        else:
            if not len(arrayofimages[i].Mag) == 0:
                magtotal += arrayofoutputs[indexImage].OgMagnitudes[i]
                phasetotal += arrayofoutputs[indexImage].OgPhaseshift[i]
                realtotal += arrayofoutputs[indexImage].Ogrealcomp[i]* arrayofcouplesliders[i][0].value() / 1000
                imagetotal += arrayofoutputs[indexImage].Ogimagcomp[i]* arrayofcouplesliders[i][1].value() / 1000
                counter+=1


    arrayofoutputs[indexImage].Mag=magtotal.copy()
    arrayofoutputs[indexImage].Phaseshift=phasetotal.copy()
    arrayofoutputs[indexImage].realcomp=realtotal.copy()
    arrayofoutputs[indexImage].imagcomp=imagetotal.copy()

    arrayofoutputs[indexImage].inversefouriertransform(indexImage,magphase)
    image = cv2.imread(f"Stuffforprogramtowork/out/{indexImage}.jpg", cv2.IMREAD_GRAYSCALE)
    arrayofoutputs[indexImage].dtype=image.dtype
    arrayofoutputs[indexImage].height, arrayofoutputs[indexImage].width=image.shape
    arrayofoutputs[indexImage].imagedata=image

    if indexImage==0:
        # if regionpercent.value()<100 and isouter:
        #     image2 = cv2.addWeighted(arrayofoutputs[indexImage].imagedata, 1.65,
        #                              np.zeros(image.shape, arrayofoutputs[indexImage].dtype), 0, 29.4)
        #     cv2.imwrite(f"Stuffforprogramtowork/out/{indexImage}Br.jpg", image2)
        #     outputImage1.setPixmap(QPixmap(f"Stuffforprogramtowork/out/{indexImage}Br.jpg"))
        # else:
        outputImage1.setPixmap(QPixmap(f"Stuffforprogramtowork/out/{indexImage}.jpg"))
    else:
        if regionpercent.value()<100 and isouter:
            image2 = cv2.addWeighted(arrayofoutputs[indexImage].imagedata, 1.65,
                                     np.zeros(image.shape, arrayofoutputs[indexImage].dtype), 0, 29.4)
            cv2.imwrite(f"Stuffforprogramtowork/out/{indexImage}Br.jpg", image2)
            outputImage1.setPixmap(QPixmap(f"Stuffforprogramtowork/out/{indexImage}Br.jpg"))
        else:
            outputImage2.setPixmap(QPixmap(f"Stuffforprogramtowork/out/{indexImage}.jpg"))



def readydataforoutput(innerregion,regionpercent):
    global arrayofimages
    if innerregion.isChecked():
        for i in range(4):
            arrayofimages[i].prepareoutput(regionpercent.value(),"in")
    else:
        for i in range(4):
            arrayofimages[i].prepareoutput(regionpercent.value(),"out")




def updategraph(isInner,regionpercent,regionpercentvalue,arrayOfGraphs,arrayOfGraphType,isclicked,index):
    # if isclicked:
    #     update_rectangle(arrayOfGraphs[index], regionpercent.value(), arrayOfGraphType, index, arrayOfGraphs, isInner)
    #     return
    global isouter
    isouter=not isInner
    percentage=regionpercent.value()
    regionpercentvalue.setText(str(percentage) + "%")
    for i in range(len(arrayOfGraphs)):
        update_rectangle(arrayOfGraphs[i], percentage,arrayOfGraphType,i,arrayOfGraphs,isInner)








def changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,whichimage,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2):
    arrayofcouplevalues[whichimage][0].setText(str(arrayofcouplesliders[whichimage][0].value()/10) +"%")
    arrayofcouplevalues[whichimage][1].setText(str(arrayofcouplesliders[whichimage][1].value()/10) + "%")

    if outputradio1.isChecked():
        UpdateOutput(self, innerregion, regionpercent, regionpercentvalue, arrayofcouplesliders, magphase, realimage,
                     outputImage1, outputImage2, 0)
    else:
        UpdateOutput(self, innerregion, regionpercent, regionpercentvalue, arrayofcouplesliders, magphase, realimage,
                     outputImage1, outputImage2, 1)





def calculatePercentage(label, sliderPercent,arrayOfGraphType,i,arrayOfGraphs,isInner,event,regionpercentvalue):
    if event.buttons() == Qt.LeftButton:
        delta_x = event.pos().x() - 0
        delta_y = event.pos().y() - 0
        delta_x = max(0.0, min(200.0, delta_x))
        delta_y = max(0.0, min(200.0, delta_y))
        if delta_x > delta_y:
            if delta_y > 100:
                delta_y = 200 - delta_y
            delta_y*=2
            percentage = 100-(delta_y / 2)
        else:
            if delta_x > 100:
                delta_x = 200 - delta_x
            delta_x*=2
            percentage = 100-(delta_x / 2)
    if not isInner:
        percentage=101-percentage
        percentage=int(percentage)
    sliderPercent.setValue(int(percentage))


def update_rectangle(label, percentage,arrayOfGraphType,i,arrayOfGraphs,isInner):
    global arrayofimages
    if len(arrayofimages[i].Mag)==0:
        return
    changetype(arrayOfGraphType,arrayOfGraphs,i)
    pixmap = label.pixmap().copy()  # Create a copy to preserve the original image
    painter = QPainter(pixmap)
    start = 2 * ((100 - percentage))
    if isInner:
        painter.setPen(QPen(Qt.red,start, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Calculate the rectangle coordinates based on the percentage
        rect = QRect(0, 0, 200,200)
    else:
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Calculate the rectangle coordinates based on the percentage
        rect = QRect(102-int(start/2), 100-int(start/2), start, start)
        painter.fillRect(rect, QColor(255, 0, 0))

    # Draw the rectangle
    painter.drawRect(rect)
    label.setPixmap(pixmap)
    painter=0



















def changetitles(arrayofcoupletitles,magphase):
    for i in range(len(arrayofcoupletitles)):
        if magphase.isChecked():
            arrayofcoupletitles[i][0].setText("Magnitude")
            arrayofcoupletitles[i][1].setText( "Phase")
        else:
            arrayofcoupletitles[i][0].setText("Real")
            arrayofcoupletitles[i][1].setText( "Imaginary")