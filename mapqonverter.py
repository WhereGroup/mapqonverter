#!/usr/bin/python2.7
# encoding: utf-8
import codecs
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

    print 'Start Writing'

    for counter, dataframe in enumerate(arcpy.mapping.ListDataFrames(mxd)):
        if counter == 0:
            print 'Creating MapSpatialReferenceSystem.'
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
        qgs_file.write(xml_document.toprettyxml(indent="    "))
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


if __name__ == "__main__":
    main()
