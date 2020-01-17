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

from qgis.utils import iface
from qgis.gui import *

import processing
import sys, os
import requests
import time

iface.mainWindow().blockSignals(True)

zlayer = ""


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
        text, okPressed = QInputDialog.getText(self, "WORKDIR", "Input your workfolder :", QLineEdit.Normal, "")
        # get path. Must be an absolute path !
        if okPressed and text != '':
            if len(text) > 3:
                WORKDIR = text
                print(text)
                return WORKDIR
        else:
            WORKDIR = "C:/Users/theo1/Documents/GitHub/Hackathon2020/mapdata/"
            print(text)
            return WORKDIR


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
        crs = layer.crs()
        crs.createFromId(4326)
        layer.setCrs(crs)
        # crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        # layer.setCrs(QgsCoordinateReferenceSystem(CRS_ID, QgsCoordinateReferenceSystem.EpsgCrsId))
        # for unknow reasons, the tif has a different Crs, but is lambert. OK.
        # layer.setCrs()

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
    # print(os.listdir(WORKDIR))
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
        print(WORKDIR)
        print(dxfName)
        print(file)
        layer = QgsVectorLayer(WORKDIR + dxfName + "|layername=entities|geometrytype=LineString", file, "ogr")
        layer.setCrs(QgsCoordinateReferenceSystem(CRS_ID, QgsCoordinateReferenceSystem.EpsgCrsId))
        QgsProject.instance().addMapLayer(layer)

        if layer.isValid() is True:
            print("Layer was loaded successfully!")
            global zlayer
            zlayer = QgsProject.instance().mapLayersByName(dxfName)[0]
            iface.setActiveLayer(zlayer)
            iface.zoomToActiveLayer()
        else:
            print("Unable to read basename and file path - Your string is probably invalid")

    except Error as e:
        print("Error loading raster file")
        print(e)


def downloadMap():
    try:
        service_url = "mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        service_uri = "type=xyz&zmin=0&zmax=21&url=https://" + requests.utils.quote(service_url)
        tms_layer = QgsRasterLayer(service_uri, "Google Satellite", "wms")
        tms_later = QgsProject.instance().addMapLayer(tms_layer)
    except Exception as e:
        print("Map failed :(")
        print(e)


app = QApplication(sys.argv)
ex = App()
ex.close()
CRS_ID = ex.getInteger()
WORKDIR = ex.getText()
# sys.exit(app.exec_())

importFirstTif()
time.sleep(2.0) 
downloadMap()
time.sleep(2.0) 
importFirstDXF()
time.sleep(2.0) 
importAllShapes()
time.sleep(2.0) 
iface.mainWindow().blockSignals(False)
iface.setActiveLayer(zlayer)
iface.zoomToActiveLayer()
