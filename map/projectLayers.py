# coding=utf-8
from _ctypes import COMError

from layer.layer import Layer as layerObj
import arcpy
import logging
from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface
from map import brokenLayers


class ProjectLayers:

    def __init__(self):
        pass

    @staticmethod
    def create_project_layers_element(xml_document, header, layer_list, arc_object_map):
        """ This creates a project layer object and its code in the dom

        It does not return anything, it just fills the dom.

        :param xml_document: the Document Object Model
        :param header: the header in the dom
        :param layer_list: the list of layers in the dataframe
        :param arc_object_map: the ArcObject Map
        """
        # Check if there are already projectlayers from another dataFrame
        project_layers_elements = xml_document.getElementsByTagName('projectlayers')
        if len(project_layers_elements) == 0:
            project_layers_element = xml_document.createElement("projectlayers")
            header.appendChild(project_layers_element)

        arcpy.AddMessage(u'%1s.\t %1s %1s \t  %1s' % ("Nr", "Name".center(50), "Status".center(33), "Typ"))

        layer_path = ''

        for index, layer in enumerate(layer_list):
            if layer.isGroupLayer:
                arcpy.AddMessage(u"{index}.\tLayer: {layer_name} ".format(
                    index=index + 1,
                    layer_name=layer.name.ljust(50)
                ))
                ProjectLayers.__create_layer_converted_message(layer, index, 'Group', xml_document)
                layer_path = ProjectLayers.__get_layer_path(layer, layer_path)
                continue
            else:
                ProjectLayers.__create_layer_element(layer, layer_list, arc_object_map, xml_document, index, layer_path)

    @staticmethod
    def __create_layer_converted_message(layer, index, layer_object_type, xml_document, error_found=False):
        """ Create a Message if succeeded or failed - and handles failure

        :param layer: the layer its all about
        :param index: its index in the layerlist
        :param layer_object_type: the type of the layer
        :param xml_document: the Document Object Model
        :param error_found: indicate if error was found - default value is false
        """
        if (layer_object_type == 'unknown') | error_found:
            status = "could not be converted"
            ProjectLayers.__handle_broken_layer(layer, xml_document)
        else:
            status = "successful converted"

        arcpy.AddMessage(
            u"{tabs} {status} \t - {type}-Layer \n".format(
                tabs=11 * "\t",
                status=status,
                type=layer_object_type.title()
            )
        )
        logging.info(
            u"{index}.\tLayer: {layer_name} {status} \t - {type} \n".format(
                index=index + 1,
                layer_name=layer.name.ljust(50),
                status=status,
                type=layer_object_type
            )
        )

    @staticmethod
    def __create_layer_element(layer, layer_list, arc_object_map, xml_document, index, layer_path):
        """ This function creates a layer_object and its content in the DOM

        :param layer: the layer its all about
        :param layer_list: the list of layers in the dataframe
        :param arc_object_map: the ArcObject Map
        :param xml_document: the Document Object Model
        :param index: the index of the layer in the layerlist
        :param layer_path: the layer_path of the layer
        """
        arcpy.AddMessage(u"{index}.\tLayer: {layer_name} ".format(
            index=index + 1,
            layer_name=layer.name.ljust(50)
        ))

        try:
            arc_layer = ProjectLayers.__get_arc_objects_layer(layer, arc_object_map)

            layer_path = ProjectLayers.__get_layer_path(layer, layer_path)

            layer_object = layerObj(layer, arc_layer, xml_document, layer_list, layer_path)

            layer_object_type = layer_object.get_layer_type()
            print layer_object_type
            base_layer_element = layer_object.create_base_layer()

            xml_document.createElement(
                layer_object.attach_layer_type(
                    layer_object_type,
                    base_layer_element
                )
            )

            ProjectLayers.__create_layer_converted_message(layer, index, layer_object_type, xml_document)
        except (KeyError, Exception):
            ProjectLayers.__create_layer_converted_message(layer, index, 'unknown', xml_document, True)

    @staticmethod
    def __get_layer_path(layer, layer_path):
        """ Returns the layer-path if possible, otherwise takes the given layer_path variable,
            which comes from a parent-layer

        For Example:
            Annotation-Layers count as Group-Layers and provide the Datasource-Path for the child layer.
            So the layer_path is a given variable and could have the information of the parent-layer.

        :param layer: the layer its all about
        :param layer_path: the path of the layer foregoing group-layer
        :return: the layer_path of the layer
        """

        if layer.supports("DATASOURCE"):
            layer_path = layer.dataSource

        return layer_path

    @staticmethod
    def __get_arc_objects_layer(layer, arc_object_map):
        """ This returns the ArcObject-Layer-Object of the (ArcPy)Layer

        :param layer: the layer its all about
        :param arc_object_map: the ArcObject Map
        :return: the ArcObject-Layer-Object
        """
        longname_layer_list = layer.longName.split("\\")
        if layer.isServiceLayer and not layer.isGroupLayer:
            longname_layer_list = longname_layer_list[0:-1]
        longname_layer_list_objects = []
        # divide the longname in the previous grouplayers and find their position
        # arcpy and arcobjects counting the layers different.
        # arcobject orientate from the parent-layers, it does not count all the childlayers from a a layer
        # arcpy just numerates every layer

        # find first layer in the longname
        for arc_index in range(arc_object_map.LayerCount):
            if longname_layer_list[0] == arc_object_map.Layer[arc_index].Name:
                try:
                    longname_layer_list_objects.append(arc_object_map.Layer[arc_index])
                    break
                except COMError:
                    ProjectLayers.__throw_unsafed_changes_error()

        # and the rest
        for index, longname_layer in enumerate(longname_layer_list[1:]):
            parent = change_interface(longname_layer_list_objects[index], ArcGisModules.module_carto.ICompositeLayer)
            for i in range(parent.Count):
                if longname_layer == parent.Layer[i].Name:
                    longname_layer_list_objects.append(parent.Layer[i])
                    break

        return longname_layer_list_objects[-1]

    @staticmethod
    def __handle_broken_layer(layer, xml_document):
        """ add a layer, which is not convertable, unknown, had errors to the broken_layers_list
            and delete its maplayer element from the dom.

        :param layer: the layer its all about
        :param xml_document: the Document Object Model
        :return:
        """
        brokenLayers.BrokenLayers.broken_layer_list.append(layer)

        map_layer_node = xml_document.getElementsByTagName('maplayer')[-1]
        parent = map_layer_node.parentNode
        parent.removeChild(map_layer_node)

    @staticmethod
    def __throw_unsafed_changes_error():
        arcpy.AddError("###################################################")
        arcpy.AddError("Alert! Are there unsafed changes in the project?")
        arcpy.AddError("Save Changes and try exporting again.")
        arcpy.AddError("###################################################")
