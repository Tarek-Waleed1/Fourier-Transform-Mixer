from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QPushButton
import pyqtgraph
import functions
import numpy as np

def initConnectors(self):
  openbutton=self.findChild(QtWidgets.QAction,"actionOpen")
  openbutton.triggered.connect(lambda: functions.browseall4(self,Imagearray,grapharray,drawtypearray))
  reset=self.findChild(QtWidgets.QAction,"actionReset")
  reset.triggered.connect(lambda: functions.resetContrastBrightness(Imagearray,outputImage1,outputImage2))


  image1=self.findChild(QtWidgets.QLabel,"inImage1")
  image2 = self.findChild(QtWidgets.QLabel, "inImage2")
  image3 = self.findChild(QtWidgets.QLabel, "inImage3")
  image4 = self.findChild(QtWidgets.QLabel, "inImage4")

  image1.mouseDoubleClickEvent = lambda event:functions.browse(self,Imagearray,grapharray,drawtypearray,0)
  image2.mouseDoubleClickEvent = lambda event:functions.browse(self,Imagearray,grapharray,drawtypearray,1)
  image3.mouseDoubleClickEvent = lambda event:functions.browse(self,Imagearray,grapharray,drawtypearray,2)
  image4.mouseDoubleClickEvent = lambda event:functions.browse(self,Imagearray,grapharray,drawtypearray,3)

  image1.start_pos = image1.mapToGlobal(image1.pos())
  image1.mousePressEvent = lambda event: functions.handle_contrast_and_brightness(event, image1,0,1)
  image1.mouseMoveEvent = lambda event: functions.handle_contrast_and_brightness(event, image1,0,1)


  image2.start_pos = image2.mapToGlobal(image2.pos())
  image2.mousePressEvent = lambda event: functions.handle_contrast_and_brightness(event, image2,1,1)
  image2.mouseMoveEvent = lambda event: functions.handle_contrast_and_brightness(event, image2,1,1)


  image3.start_pos = image3.mapToGlobal(image3.pos())
  image3.mousePressEvent = lambda event: functions.handle_contrast_and_brightness(event, image3,2,1)
  image3.mouseMoveEvent = lambda event: functions.handle_contrast_and_brightness(event, image3,2,1)


  image4.start_pos = image4.mapToGlobal(image4.pos())
  image4.mousePressEvent = lambda event: functions.handle_contrast_and_brightness(event, image4,3,1)
  image4.mouseMoveEvent = lambda event: functions.handle_contrast_and_brightness(event, image4,3,1)

  graph1 = self.findChild(QtWidgets.QLabel, "Graph1")
  graph2 = self.findChild(QtWidgets.QLabel, "Graph2")
  graph3 = self.findChild(QtWidgets.QLabel, "Graph3")
  graph4 = self.findChild(QtWidgets.QLabel, "Graph4")
  drawtype1=self.findChild(QtWidgets.QComboBox,"inType1")
  drawtype2 = self.findChild(QtWidgets.QComboBox, "inType2")
  drawtype3 = self.findChild(QtWidgets.QComboBox, "inType3")
  drawtype4 = self.findChild(QtWidgets.QComboBox, "inType4")

  sendTo1 = self.findChild(QtWidgets.QPushButton,"sendto1")
  sendTo2 = self.findChild(QtWidgets.QPushButton,"sendto2")
  tabIndex = self.findChild(QtWidgets.QTabWidget,"Modes")
  sendTo1.clicked.connect(lambda: functions.sendToOutput(self,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2,0))
  sendTo2.clicked.connect(lambda: functions.sendToOutput(self,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2,1))
  drawtype1.currentIndexChanged.connect(lambda :functions.changetype(drawtypearray,grapharray,0))
  drawtype2.currentIndexChanged.connect(lambda :functions.changetype(drawtypearray,grapharray,1))
  drawtype3.currentIndexChanged.connect(lambda :functions.changetype(drawtypearray,grapharray,2))
  drawtype4.currentIndexChanged.connect(lambda :functions.changetype(drawtypearray,grapharray,3))

  Imagearray=[image1,image2,image3,image4]
  grapharray=[graph1,graph2,graph3,graph4]
  drawtypearray=[drawtype1,drawtype2,drawtype3,drawtype4]


  regionpercent=self.findChild(QtWidgets.QSlider,"percentcontrol")
  regionpercentvalue=self.findChild(QtWidgets.QLabel,"percentValue")
  regionpercent.setRange(1,100)

  regionpercent.valueChanged.connect(lambda:  functions.updategraph(innerregion.isChecked(),regionpercent,regionpercentvalue,grapharray,drawtypearray,0,False))

  innerregion=self.findChild(QtWidgets.QRadioButton,"InnerRadio")
  innerregion.toggled.connect(lambda: functions.readydataforoutput(innerregion,regionpercent))

  graph1.start_pos = graph1.mapToGlobal(graph1.pos())
  graph1.mousePressEvent = lambda event: functions.calculatePercentage(graph1, regionpercent, drawtypearray,0,grapharray,innerregion.isChecked(),event,regionpercentvalue)
  graph1.mouseMoveEvent = lambda event: functions.calculatePercentage(graph1, regionpercent, drawtypearray,0,grapharray,innerregion.isChecked(),event,regionpercentvalue)

  graph2.start_pos = graph2.mapToGlobal(graph2.pos())
  graph2.mousePressEvent = lambda event: functions.calculatePercentage(graph2, regionpercent, drawtypearray,1,grapharray,innerregion.isChecked(),event,regionpercentvalue)
  graph2.mouseMoveEvent = lambda event: functions.calculatePercentage(graph2, regionpercent, drawtypearray,1,grapharray,innerregion.isChecked(),event,regionpercentvalue)

  graph3.start_pos = graph3.mapToGlobal(graph3.pos())
  graph3.mousePressEvent = lambda event: functions.calculatePercentage(graph3, regionpercent, drawtypearray,2,grapharray,innerregion.isChecked(),event,regionpercentvalue)
  graph3.mouseMoveEvent = lambda event: functions.calculatePercentage(graph3, regionpercent, drawtypearray,2,grapharray,innerregion.isChecked(),event,regionpercentvalue)

  graph4.start_pos = graph4.mapToGlobal(graph4.pos())
  graph4.mousePressEvent = lambda event: functions.calculatePercentage(graph4, regionpercent, drawtypearray,3,grapharray,innerregion.isChecked(),event,regionpercentvalue)
  graph4.mouseMoveEvent = lambda event: functions.calculatePercentage(graph4, regionpercent, drawtypearray,3,grapharray,innerregion.isChecked(),event,regionpercentvalue)





  scalecontrol1_1 = self.findChild(QtWidgets.QSlider, "control1_3")
  scalecontrol1_2 = self.findChild(QtWidgets.QSlider, "control1_4")
  scalecontrol2_1 = self.findChild(QtWidgets.QSlider, "control2_3")
  scalecontrol2_2 = self.findChild(QtWidgets.QSlider, "control2_4")
  scalecontrol3_1 = self.findChild(QtWidgets.QSlider, "control3_3")
  scalecontrol3_2 = self.findChild(QtWidgets.QSlider, "control3_4")
  scalecontrol4_1 = self.findChild(QtWidgets.QSlider, "control4_3")
  scalecontrol4_2 = self.findChild(QtWidgets.QSlider, "control4_4")



  title1_1 = self.findChild(QtWidgets.QLabel, "title1_3")
  title1_2 = self.findChild(QtWidgets.QLabel, "title1_4")
  title2_1 = self.findChild(QtWidgets.QLabel, "title2_3")
  title2_2 = self.findChild(QtWidgets.QLabel, "title2_4")
  title3_1 = self.findChild(QtWidgets.QLabel, "title3_3")
  title3_2 = self.findChild(QtWidgets.QLabel, "title3_4")
  title4_1 = self.findChild(QtWidgets.QLabel, "title4_3")
  title4_2 = self.findChild(QtWidgets.QLabel, "title4_4")

  value1_1 = self.findChild(QtWidgets.QLabel, "value1_3")
  value1_2 = self.findChild(QtWidgets.QLabel, "value1_4")
  value2_1 = self.findChild(QtWidgets.QLabel, "value2_3")
  value2_2 = self.findChild(QtWidgets.QLabel, "value2_4")
  value3_1 = self.findChild(QtWidgets.QLabel, "value3_3")
  value3_2 = self.findChild(QtWidgets.QLabel, "value3_4")
  value4_1 = self.findChild(QtWidgets.QLabel, "value4_3")
  value4_2 = self.findChild(QtWidgets.QLabel, "value4_4")


  arrayofcoupletitles=[(title1_1,title1_2),(title2_1,title2_2),(title3_1,title3_2),(title4_1,title4_2)]
  arrayofcouplevalues = [(value1_1, value1_2), (value2_1, value2_2), (value3_1, value3_2), (value4_1, value4_2)]






  arrayofcouplesliders=[(scalecontrol1_1,scalecontrol1_2),(scalecontrol2_1,scalecontrol2_2),(scalecontrol3_1,scalecontrol3_2),(scalecontrol4_1,scalecontrol4_2)]

  magphase=self.findChild(QtWidgets.QRadioButton,"magPhase_2")
  realimage=self.findChild(QtWidgets.QRadioButton,"realImg_2")
  magphase.toggled.connect(lambda: functions.changetitles(arrayofcoupletitles,magphase))


  outputImage1=self.findChild(QtWidgets.QLabel,"outImage1_3")
  outputImage2=self.findChild(QtWidgets.QLabel,"outImage2_2")

  outputImage1.start_pos = outputImage1.mapToGlobal(outputImage1.pos())
  outputImage1.mousePressEvent = lambda event: functions.handle_contrast_and_brightness(event, outputImage1, 0,0)
  outputImage1.mouseMoveEvent = lambda event: functions.handle_contrast_and_brightness(event, outputImage1, 0,0)

  outputImage2.start_pos = outputImage2.mapToGlobal(outputImage2.pos())
  outputImage2.mousePressEvent = lambda event: functions.handle_contrast_and_brightness(event, outputImage2, 1,0)
  outputImage2.mouseMoveEvent = lambda event: functions.handle_contrast_and_brightness(event, outputImage2, 1,0)

  outputradio1=self.findChild(QtWidgets.QRadioButton,"radioOut_2")
  outputradio2 = self.findChild(QtWidgets.QRadioButton, "radioOut2_2")



  scalecontrol1_1.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,0,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))
  scalecontrol1_2.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,0,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))
  scalecontrol2_1.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,1,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))
  scalecontrol2_2.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,1,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))
  scalecontrol3_1.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,2,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))
  scalecontrol3_2.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,2,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))
  scalecontrol4_1.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,3,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))
  scalecontrol4_2.valueChanged.connect(lambda: functions.changevalueofslidersandupdate(self,outputradio1,arrayofcouplevalues,3,innerregion,regionpercent,regionpercentvalue,arrayofcouplesliders,magphase,realimage,outputImage1,outputImage2))








