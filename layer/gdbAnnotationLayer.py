from gdbFilePathProvider import GdbFilePathProvider
from renderer.renderer import Renderer as rendererObj


class GDBAnnotationLayer:
    def __init__(self):
        pass

    @staticmethod
    def create_gdb_annotation_layer_content(base, map_layer_element):
        """ This Function creates gdb-layer specific content in the
            fitting maplayer-element

        :param base: Is the self from the LayerObject
        :param map_layer_element: the map_layer_element in the DOM
        """
        map_layer_element.setAttribute("type", "vector")
        map_layer_element.setAttribute("geometry", "Polygon")
        map_layer_element.setAttribute("labelsEnabled", "1")
    
        for datasource, provider in zip(map_layer_element.getElementsByTagName('datasource'),
                                        map_layer_element.getElementsByTagName('provider')):
            provider.setAttribute("encoding", "UTF-8")
            provider.appendChild(base.xml_document.createTextNode("ogr"))
            absolute_path_to_gdb_layer = base.gdb_path
            layer_path = GdbFilePathProvider.create_layer_path_from_gdb_path(absolute_path_to_gdb_layer)
            datasource_content = base.xml_document.createTextNode(layer_path)
            datasource.appendChild(datasource_content)
    
        rendererObj(base.xml_document, map_layer_element, base.arc_layer, base.layer, "gdb").get_renderer()
