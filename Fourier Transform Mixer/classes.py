from PyQt5 import QtGui, QtCore, QtWidgets
import csv
from PyQt5.QtWidgets import QFileDialog, QColorDialog,QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import numpy as np
import pandas as pd
import random
from PIL import Image
import os
from functools import partial
from random import randint
from scipy.signal import resample
from PyQt5.QtGui import QPixmap,QImage
import cv2

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *





class image():
    def __init__(self):
       self.imagedata=[]
       self.height=[]
       self.width=[]
       self.dtype=[]
       #datapart
       self.frequency=[]
       self.Mag = []
       self.Phaseshift = []
       self.realcomp=[]
       self.imagcomp=[]

       #imagepart
       self.image=[]
       self.magimage=[]
       self.phaseimage=[]
       self.realcompimage=[]
       self.imagcompimage=[]
       #stuff to go out
       self.constraintmag=[]
       self.constraintphase=[]
       self.constraintreal=[]
       self.constraintimaginary=[]


       self.OgMagnitudes=[]
       self.OgPhaseshift = []
       self.Ogrealcomp = []
       self.Ogimagcomp = []







    def readydata(self):
        f_transform = np.fft.fft2( self.imagedata)
        fourier_shift = np.fft.fftshift(f_transform)
        self.Mag=np.abs(fourier_shift)
        self.Phaseshift=np.angle(fourier_shift)
        self.realcomp= np.real(fourier_shift)
        self.imagcomp = np.imag(fourier_shift)
        self.getimage()

    def scale_and_shift(self, data):
        # Scale and shift the data to the range [0, 255]
        scaled_data = 255 * (data - np.min(data)) / (np.max(data) - np.min(data))
        return scaled_data.astype(np.uint8)

    def getimage(self):
        # #normalize some stuff
        # magnitude_spectrum_normalized = 255 * (self.Mag/ np.max(self.Mag))
        # Phase_normalized=(self.Phaseshift + np.pi) * (255 / (2 * np.pi))
        # #turn to unit8 to get qpixmaps
        # real_part_image = np.uint8(self.realcomp)
        # imaginary_part_image = np.uint8(self.imagcomp)
        # phase_spectrum_image = np.uint8(Phase_normalized)
        # magnitude_spectrum_image = np.uint8(magnitude_spectrum_normalized)

        # self.magimage = self.nparray_to_qpixmap(magnitude_spectrum_image)
        # self.phaseimage = self.nparray_to_qpixmap(real_part_image)
        # self.realcompimage = self.nparray_to_qpixmap(imaginary_part_image)
        # self.imagcompimage = self.nparray_to_qpixmap(phase_spectrum_image)
        magnitude_spectrum_normalized = self.scale_and_shift(np.log(self.Mag+1))
        phase_normalized = self.scale_and_shift(self.Phaseshift)
        real_part_image = self.scale_and_shift(self.realcomp)
        imaginary_part_image = self.scale_and_shift(self.imagcomp)
        # Convert NumPy arrays to bytes
        mag_bytes = magnitude_spectrum_normalized.tobytes()
        phase_bytes = phase_normalized.tobytes()
        real_bytes = real_part_image.tobytes()
        imag_bytes = imaginary_part_image.tobytes()

        # Create QImage objects
        self.magimage = QImage(mag_bytes, self.width, self.height, QImage.Format_Grayscale8)
        self.phaseimage = QImage(phase_bytes, self.width, self.height, QImage.Format_Grayscale8)
        self.realcompimage = QImage(real_bytes, self.width, self.height, QImage.Format_Grayscale8)
        self.imagcompimage = QImage(imag_bytes, self.width, self.height, QImage.Format_Grayscale8)



# def nparray_to_qpixmap(self,stuff):
    #     height, width = stuff.shape
    #     bytes_per_line = 1 * width
    #     q_image = QImage(stuff.data.tobytes(), width, height, QImage.Format_Grayscale8)
    #     return QPixmap.fromImage(q_image)




    def prepareoutput(self,percentofstuff,condition):
        self.constraintmag=self.addconstraint(self.Mag,percentofstuff,condition)
        self.constraintphase = self.addconstraint(self.Phaseshift, percentofstuff, condition)
        self.constraintreal = self.addconstraint(self.realcomp, percentofstuff, condition)
        self.constraintimaginary = self.addconstraint(self.imagcomp, percentofstuff, condition)

    def addconstraint(self,array,per,condition):
        if per==100:
            return (array)

        if len(array)==0:
            return 0
        Temp=array
        percentile=(100-per)/(100)
        length=int(percentile*len(Temp)/2)
        returnarray = Temp.copy()




        if condition=="in":
            returnarray[0:length]=0
            returnarray[-length:-1]=0
            return returnarray
        else:
            returnarray[int(len(returnarray)/2):int(len(returnarray)/2)+length//3-1]=0
            returnarray[int(len(returnarray) / 2) - length//3 + 1:int(len(returnarray) / 2)] = 0
            return returnarray










    def inversefouriertransform(self,number,check):
        if not check.isChecked():
            complex_array = self.realcomp +1j * self.imagcomp
            inversesfitcomplexarray=np.fft.ifftshift(complex_array)
            self.imagedata=np.fft.ifft2(inversesfitcomplexarray)
            rel=np.real(self.imagedata)
            normalized=cv2.normalize(rel,None,0,255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imwrite(f"Stuffforprogramtowork/out/{number}.jpg", normalized)
            image=Image.open(f"Stuffforprogramtowork/out/{number}.jpg")
            new_image=image.resize((400,400))
            new_image.save(f"Stuffforprogramtowork/out/{number}.jpg")



        else:

            Mixed_FT = np.multiply( 10*self.Mag, np.exp(1j *self.Phaseshift))
            Inverse_fourier_image = np.real(np.fft.ifft2(np.fft.ifftshift(Mixed_FT)))
            Inverse_fourier_image = cv2.normalize(Inverse_fourier_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imwrite(f"Stuffforprogramtowork/out/{number}.jpg", Inverse_fourier_image)
            image=Image.open(f"Stuffforprogramtowork/out/{number}.jpg")
            new_image=image.resize((400,400))
            new_image.save(f"Stuffforprogramtowork/out/{number}.jpg")















    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     pixmap = QPixmap("myPic.png")
    #     painter.drawPixmap(self.rect(), pixmap)
    #     pen = QPen(Qt.red, 3)
    #     painter.setPen(pen)
    #     painter.drawLine(10, 10, self.rect().width() - 10, 10)






    def emptydata(self):
        self.imagedata = []
        self.height = []
        self.width = []
        # datapart
        self.frequency = []
        self.Mag = []
        self.Phaseshift = []
        self.realcomp = []
        self.imagcomp = []

        # imagepart
        self.image = []
        self.magimage = []
        self.phaseimage = []
        self.realcompimage = []
        self.imagcompimage = []
        # stuff to go out
        self.constraintmag = []
        self.constraintphase = []
        self.constraintreal = []
        self.constraintimaginary = []

        self.OgMagnitudes = []
        self.OgPhaseshift = []
        self.Ogrealcomp = []
        self.Ogimagcomp = []
