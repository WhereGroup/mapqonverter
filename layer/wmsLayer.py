import arcpy

from modules.functions import change_interface
from modules.arcGisModules import ArcGisModules
from renderer.renderer import Renderer as rendererObj


class WMSLayer:
    def __init__(self):
        pass

    @staticmethod
    def create_wms_layer_content(base, map_layer_element):
        """ This Function creates wms-layer specific content in the
            fitting maplayer-element

        :param base: Is the self from the LayerObject
        :param map_layer_element: the maplayer_element in the DOM
        """
        map_layer_element.setAttribute("type", "raster")
        wms_layer = change_interface(base.arc_layer, ArcGisModules.module_carto.IWMSGroupLayer)
        try:
            wms_layer_version = wms_layer.WMSServiceDescription.WMSVersion
        except ValueError:
            arcpy.AddWarning(
                "\t\tWMS could not load version. Are you working offline? Default Version is 1.3.0"
            )
            wms_layer_version = "1.3.0"

        for datasource_element, srid_element, provider_element \
                in zip(map_layer_element.getElementsByTagName('datasource'),
                       map_layer_element.getElementsByTagName('srid'),
                       map_layer_element.getElementsByTagName('provider')):
            provider_element.appendChild(base.xml_document.createTextNode("wms"))
            data_source_content = ("crs=EPSG:" + srid_element.firstChild.nodeValue +
                                   "&dpiMode=7&format=image/png&layers=" + base.layer.serviceProperties["Name"] +
                                   "&styles=&url=" + base.layer.serviceProperties["URL"] + "version%3D" +
                                   wms_layer_version)
            data_source_content = base.xml_document.createTextNode(data_source_content)
            datasource_element.appendChild(data_source_content)

        rendererObj(base.xml_document, map_layer_element, base.arc_layer, base.layer, "wms").get_renderer()
