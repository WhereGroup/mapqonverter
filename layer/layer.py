from wmsLayer import WMSLayer
from gdbAnnotationLayer import GDBAnnotationLayer
from rasterLayer import RasterLayer
from featureLayer import FeatureLayer
from databaseLayer import DatabaseLayer
from layerSrs import LayerSrs


class Layer:

    def __init__(self, layer, arc_layer, xml_document, layer_list, gdb_path="placeholder"):
        self.layer = layer
        self.arc_layer = arc_layer
        self.xml_document = xml_document
        self.gdb_path = gdb_path
        self.layer_list = layer_list

    def create_base_layer(self):
        """ This creates a maplayer-Element in the DOM with basic configuration

        :return: the map_layer_element
        """
        layer_id = self.layer.longName + str(20190727170816078)
        layer_name = self.layer.name
        project_layers_element = self.xml_document.getElementsByTagName("projectlayers")[0]

        map_layer_element = self.xml_document.createElement("maplayer")
        map_layer_element.setAttribute("minScale", "1e+08")
        map_layer_element.setAttribute("maxScale", "0")
        map_layer_element.setAttribute("minLabelScale", "1e+08")
        map_layer_element.setAttribute("maxLabelScale", "0")
        map_layer_element.setAttribute("hasScaleBasedVisibilityFlag", "0")
        map_layer_element.setAttribute("scaleBasedLabelVisibilityFlag", "0")
        project_layers_element.appendChild(map_layer_element)

        id_element = self.xml_document.createElement("id")
        id_element.appendChild(self.xml_document.createTextNode(layer_id))
        map_layer_element.appendChild(id_element)

        data_source_element = self.xml_document.createElement("datasource")
        map_layer_element.appendChild(data_source_element)

        layer_name_element = self.xml_document.createElement("layername")
        layer_name_content = self.xml_document.createTextNode(layer_name)
        layer_name_element.appendChild(layer_name_content)
        map_layer_element.appendChild(layer_name_element)

        srs_element = self.xml_document.createElement("srs")
        map_layer_element.appendChild(srs_element)

        LayerSrs.create_layer_srs(self, srs_element)

        provider_element = self.xml_document.createElement("provider")
        map_layer_element.appendChild(provider_element)

        return map_layer_element

    def get_layer_type(self):
        """ The function analyzes the layer and returns its type

        :return: the layer_type
        """
        layer_type = ""
        if self.layer.isFeatureLayer:
            if self.layer.dataSource[:8] == 'Database':
                layer_type = "database"
            else:
                layer_type = "feature"
        elif self.layer.isRasterLayer:
            layer_type = "raster"
        elif self.layer.isServiceLayer:
            layer_type = "wms"
        elif ".gdb" in self.gdb_path:
            layer_type = "gdb"
        else:
            layer_type = "unknown"

        return layer_type

    dict_layers = {
        'feature': FeatureLayer.create_feature_layer_content,
        'raster': RasterLayer.create_raster_layer_content,
        'wms': WMSLayer.create_wms_layer_content,
        'gdb': GDBAnnotationLayer.create_gdb_annotation_layer_content,
        'database': DatabaseLayer.create_database_layer_content
    }

    def attach_layer_type(self, layer_type, map_layer_element):
        """ This function creates layer-type specific configurations in the DOM

        :param layer_type: the type if the layer
        :param map_layer_element: the maplayer element in the DOM
        """
        try:
            self.dict_layers[layer_type](self, map_layer_element)
        except KeyError:
            self.__adapt_unknown_layer()

    @staticmethod
    def __adapt_unknown_layer():
        """ This is a place to log unknown layers for the user or developer.
            TODO Really Log it
        """
        print "This is an unknown Layer!"
