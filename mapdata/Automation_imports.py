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

from PyQt5.QtGui import *

from PyQt5.QtCore import (QCoreApplication,
                          QFileInfo,
                          QSettings)

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QPushButton, QButtonGroup, QAbstractButton, QFileDialog

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

from qgis.utils import iface
from qgis.gui import *

import processing
import sys, os
import requests
import time

iface.mainWindow().blockSignals(True)

CRS_ID = 2154
WORKDIR = "" # Ici, le chemin à changer

ZLAYER = 0


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Qgis Dialogs'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.getInteger()
        # self.getText()

        self.show()

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "CRS ID", "Input a valid CRS ID:", 2154, 0, 999999, 1)
        if okPressed:
            if i > 1:
                CRS_ID = i
                print(i)
                return CRS_ID
        else:
            CRS_ID = 2154
            print(i)
            return CRS_ID


    def getText(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Pidate u WORKDIR")) # Waaaaaay better. Picks a directory
        print(folder)
        return folder
        

def importAllTifs():
    # import all Tif found in this folder
    localfolder = os.listdir(WORKDIR + '/tifs/')
    tifs = []

    for tif in localfolder:
        if tif[-4:] == ".tif" or tif[-4:] == ".TIF":
            tifs.append(tif)

    print("Tifs Found : " + str(len(tifs)))

    try:
        for tif in tifs:
            print(localfolder)
            print(tif)

            fileInfo = QFileInfo(WORKDIR + '/tifs/' + tif)
            path = fileInfo.filePath()
            basename = fileInfo.baseName()
            layer = QgsRasterLayer(path, basename)
            crs = layer.crs()
            crs.createFromId(4326)
            layer.setCrs(crs)

            QgsProject.instance().addMapLayer(layer)

            if layer.isValid() is True:
                print("Layer was loaded successfully!")
            else:
                print("Unable to read basename and file path - Your string is probably invalid")

    except Exception as e:
        print("Error loading raster file")
        print(e)


def importAllShapes():
    # import all the shp files in the shapes folder
    # print(os.listdir(WORKDIR))
    shapesfolder = os.listdir(WORKDIR + '/shapes/')
    shapes = []

    for shape in shapesfolder:
        if shape[-4:] == ".SHP" or shape[-4:] == ".shp":
            shapes.append(shape)

    try:
        for shapeF in shapes:
            print(WORKDIR + "/shapes/" + shapeF)

            path_to_ports_layer = WORKDIR + "/shapes/" + shapeF

            # The format is:
            # vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

            vlayer = QgsVectorLayer(path_to_ports_layer, shapeF, "ogr")
            vlayer.setCrs(QgsCoordinateReferenceSystem(CRS_ID, QgsCoordinateReferenceSystem.EpsgCrsId))
            QgsProject.instance().addMapLayer(vlayer)
            if not vlayer.isValid():
                print("Layer failed to load!")

    except Exception as e:
        "An error occured when loading the shapes files"
        print(e)


def importAllDXF():
    # import the first Tif found in this folder
    localfolder = os.listdir(WORKDIR + '/dxfs/')
    # These lines allow you to set a breakpoint in the app
    dxfName = []

    for dxf in localfolder:
        if dxf[-4:] == ".dxf" or dxf[-4:] == ".DXF":
            dxfName.append(dxf)
    
    print("DFX Found : " + str(len(dxfName)))

    try:
        for dxf in dxfName:
            print(localfolder)
            print(dxf)
            layer = QgsVectorLayer(WORKDIR + '/dxfs/' + dxf + "|layername=entities|geometrytype=LineString", dxf, "ogr")
            layer.setCrs(QgsCoordinateReferenceSystem(CRS_ID, QgsCoordinateReferenceSystem.EpsgCrsId))
            QgsProject.instance().addMapLayer(layer)

            if layer.isValid() is True:
                print("Layer was loaded successfully!")
                ZLAYER = QgsProject.instance().mapLayersByName(dxf)[0]
                iface.setActiveLayer(ZLAYER)
                iface.zoomToActiveLayer()
            else:
                print("Unable to read basename and file path - Your string is probably invalid")

    except Exception as e:
        print("Error loading raster file")
        print(e)


def downloadMap():
    try:
        service_url = "mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        service_uri = "type=xyz&zmin=0&zmax=21&url=https://" + requests.utils.quote(service_url)
        tms_layer = QgsRasterLayer(service_uri, "Google Satellite", "wms")
        tms_layer = QgsProject.instance().addMapLayer(tms_layer)
    except Exception as e:
        print("Map failed :(")
        print(e)


app = QApplication(sys.argv)
ex = App()
ex.close()
CRS_ID = ex.getInteger()
w_temp = ex.getText()

if w_temp != None:
    WORKDIR = w_temp

#All_Tifs = ex.allT()
#All_DXF = ex.allD()
#sys.exit(app.exec_())

#if All_Tifs == False:
importAllTifs()
    
time.sleep(2.0) 
downloadMap()
time.sleep(2.0) 

#if All_DXF == False:
importAllDXF()
    
time.sleep(2.0) 
importAllShapes()
time.sleep(2.0) 
iface.mainWindow().blockSignals(False)
