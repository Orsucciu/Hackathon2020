# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from PyQt5.QtCore import (QCoreApplication,
                        QFileInfo,
                        QSettings)

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsRasterLayer,
                       QgsProject,
                       QgsVectorLayer,
                       QgsCoordinateReferenceSystem)
import processing
import sys, os

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 input dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.getInteger()
        self.getText()
        
        self.show()
        
    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "CRS ID","Input a valid CRS ID:", 28, 0, 999999999, 1)
        if okPressed:
            CRS_ID = i
            print(i)

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "WORKDIR","Input your workfolder :", QLineEdit.Normal, "")
        if okPressed and text != '':
            WORKDIR = text
            print(text)
            

WORKDIR = "C:/Users/theo1/Documents/GitHub/Hackathon2020/mapdata/"
CRS_ID = 2154 # CRS id we'll apply to all layers. This is lambert

def importFirstTif():
    # import the first Tif found in this folder
    localfolder = os.listdir(WORKDIR)
    tifName = ""
    
    for file in localfolder:
        if file[-4:] == ".tif" or file[-4:] == ".TIF":
            tifName = file
            break
    
    print("TIFNAME : " + tifName)
    
    try:
        fileInfo = QFileInfo(WORKDIR + tifName)
        path = fileInfo.filePath()
        basename = fileInfo.baseName()
        layer = QgsRasterLayer(path, basename)
        layer.setCrs(QgsCoordinateReferenceSystem(CRS_ID, QgsCoordinateReferenceSystem.EpsgCrsId))
        
        QgsProject.instance().addMapLayer(layer)
        
        if layer.isValid() is True:
            print("Layer was loaded successfully!")
        else:
            print("Unable to read basename and file path - Your string is probably invalid")
        
    except Error as e:
        print("Error loading raster file")
        print(e)

def importAllShapes():
    # import all the shp files in the shapes folder
    #print(os.listdir(WORKDIR))
    shapesfolder = os.listdir(WORKDIR + '/shapes/')
    shapes = []
    
    for file in shapesfolder:
        if file[-4:] == ".SHP" or file[-4:] == ".shp":
            shapes.append(file)
    
    try:
        for shapeF in shapes:
            print(WORKDIR + "shapes/" + shapeF)
            
            path_to_ports_layer = WORKDIR + "shapes/" + shapeF

            # The format is:
            # vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

            vlayer = QgsVectorLayer(path_to_ports_layer, shapeF, "ogr")
            vlayer.setCrs(QgsCoordinateReferenceSystem(CRS_ID, QgsCoordinateReferenceSystem.EpsgCrsId))
            QgsProject.instance().addMapLayer(vlayer)
            if not vlayer.isValid():
                print("Layer failed to load!")
        
    except:
        "An error occured when loading the shapes files"

def importFirstDXF():
    # import the first Tif found in this folder
    localfolder = os.listdir(WORKDIR)
    dxfName = ""
    
    for file in localfolder:
        if file[-4:] == ".dxf" or file[-4:] == ".DXF":
            dxfName = file
            break
    
    try:

        layer = QgsVectorLayer(WORKDIR + file + "|layername=entities|geometrytype=LineString", file, "ogr")
        layer.setCrs(QgsCoordinateReferenceSystem(CRS_ID, QgsCoordinateReferenceSystem.EpsgCrsId))
        QgsProject.instance().addMapLayer(layer)
        
        if layer.isValid() is True:
            print("Layer was loaded successfully!")
        else:
            print("Unable to read basename and file path - Your string is probably invalid")
        
    except Error as e:
        print("Error loading raster file")
        print(e)

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())

importFirstTif()
importFirstDXF()
importAllShapes()