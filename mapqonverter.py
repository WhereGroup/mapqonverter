#!/usr/bin/python2.7
# encoding: utf-8
# Mxd2Qgs ver 3.1
# Copyright (C) 2011 Allan Maungu
# Modified by: Peter Heidelbach, Stefan Giese
# EMAIL: lumtegis (at) gmail.com
# WEB  : http://geoscripting.blogspot.com
# WEB  : wheregroup.com
# Usage : Exporting current ArcMap document layers to QGIS file
# The resulting file can be opened in QGIS
# Tested on ArcMap 10.7, Python 2.7.10 and QGIS 3.10.0 'A Coruna'
# ----------------------------------------------------------
# Mxd2Qgs ver 2.0
# Copyright (C) 2011 Allan Maungu
# Modified by: Shiuli Pervin
# EMAIL: lumtegis (at) gmail.com
# WEB  : http://geoscripting.blogspot.com
# Usage : Exporting current ArcMap document layers to Quantum GIS file
# The resulting file can be opened in Quantum GIS
# Tested on ArcMap 10.4, Python 2.7.10 and Quantum GIS 2.18.13 'Las Palmas'
# ----------------------------------------------------------
# Mxd2Qgs ver 1.0
# Copyright (C) 2011 Allan Maungu
# EMAIL: lumtegis (at) gmail.com
# WEB  : http://geoscripting.blogspot.com
# Usage : Exporting current ArcMap document layers to Quantum GIS file
# The resulting file can be opened in Quantum GIS
# Tested on ArcMap 10, Python 2.6.5 and Quantum GIS 1.6.0
# -----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ---------------------------------------------------------------------
import codecs
import xml
from xml.dom.minidom import Document
from zipfile import ZipFile
import os
import arcpy
from comtypes.client import CreateObject

from map import brokenLayers
from map.layerTree import LayerTree
from modules.functions import type_cast_module
from modules.arcGisModules import ArcGisModules
from map.header import create_header
from map.mapSpatialReferenceSystem import MapSpatialReferenceSystem
from map.mapLegend import MapLegend
from map.mapProperties import MapProperties
from map.projectLayers import ProjectLayers


def main():
    """ This is the main script to convert a ArcMap-Project"""
    export_name = arcpy.GetParameterAsText(0)

    if export_name.endswith(".qgs") or export_name.endswith(".qgz"):
        export_name_short = export_name[:-4]

    qgs_file_name = "{}.qgs".format(export_name_short)
    qgs_file = codecs.open(qgs_file_name, "w", encoding="utf-8")

    xml_document = Document()

    header = create_header(xml_document)

    arcpy.AddMessage("Scanning Project and collecting Layer-Information")

    # take Infos from opened Arcgis -> to access the arcobjects
    # a reference to the ArcMap application
    arc_app = CreateObject(ArcGisModules.module_framework.AppROT, interface=ArcGisModules.module_framework.IAppROT)
    arc_doc = type_cast_module(arc_app.Item(0).Document, ArcGisModules.module_map_ui.IMxDocument)
    arc_doc_info = type_cast_module(arc_doc, ArcGisModules.module_carto.IDocumentInfo2)

    project_path = ""
    try:
        project_path = os.path.dirname(arc_doc_info.Folder)
    except TypeError:
        print "There is no ArcMap-Project open - Will Crash!"
    arcpy.env.workspace = project_path
    arcpy.env.overwriteOutput = True

    # this is the arcpy connection to the document
    mxd_path = os.path.join(arc_doc_info.Path)
    mxd = arcpy.mapping.MapDocument(mxd_path)

    print 'Converting mxd........'

    for counter, dataframe in enumerate(arcpy.mapping.ListDataFrames(mxd)):
        if counter == 0:
            print 'Creating MapSpatialReferenceSystem........'
            MapSpatialReferenceSystem.create_map_srs_element(xml_document, header, dataframe)

        arc_dataframe = arc_doc.Maps.Item[counter]
        layer_list = arcpy.mapping.ListLayers(dataframe)

        arcpy.AddMessage("{} Layers are in the Dataframe".format(str(len(layer_list))))

        ProjectLayers.create_project_layers_element(xml_document, header, layer_list, arc_dataframe)
        broken_layer_list = brokenLayers.BrokenLayers.broken_layer_list
        for broken_layer in broken_layer_list:
            if broken_layer in layer_list:
                layer_list.remove(broken_layer)
        MapLegend.create_map_legend_element(xml_document, header, layer_list, dataframe)
        LayerTree.create_layertree(xml_document, header, layer_list, dataframe)
        MapProperties.create_map_properties_element(xml_document, header)

    try:
        xml_document.writexml(qgs_file, indent='  ', addindent='  ', newl='\n', encoding='UTF-8')
        arcpy.AddMessage("Project saved!")
        arcpy.AddMessage('QGIS-File written')
    finally:
        qgs_file.close()

    if export_name.endswith(".qgz"):
        qgd_file_name = "{}.qgd".format(export_name_short)
        qgd_file = open(qgd_file_name, "w")
        qgd_file.close()

        with ZipFile("{}.qgz".format(export_name_short), "w") as newzip:
            newzip.write(qgs_file_name, os.path.basename(qgs_file.name))
            newzip.write(qgd_file_name, os.path.basename(qgd_file.name))

        print 'and zipped.'
        try:
            os.remove(qgs_file_name)
            os.remove(qgd_file_name)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))


def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    """ This functions has fixed formatting for the created XML-File
    :param writer = the file to write to
    :param indent = current indentation
    :param addindent = indentation to add to higher levels
    :param newl = newline string
    """
    writer.write(indent+"<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        xml.dom.minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
          and self.childNodes[0].nodeType == xml.dom.minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % newl)
        for node in self.childNodes:
            node.writexml(writer, indent+addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % newl)


xml.dom.minidom.Element.writexml = fixed_writexml


if __name__ == "__main__":
    main()
