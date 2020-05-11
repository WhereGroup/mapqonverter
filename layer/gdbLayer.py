from renderer.renderer import Renderer as rendererObj


class GDBLayer:
    def __init__(self):
        pass

    @staticmethod
    def create_gdb_layer_content(base, map_layer_element):
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
            provider.appendChild(base.document.createTextNode("ogr"))
            datasource_path = base.gdb_path

            geo_data_base_name = datasource_path.split("\\")[-2]
            geo_data_base_layer_name = datasource_path.split("\\")[-1]
            ds = base.document.createTextNode("./" + geo_data_base_name + "|layername=" + geo_data_base_layer_name)
            datasource.appendChild(ds)
    
        rendererObj(base.document, map_layer_element, base.arc_layer, base.layer, "gdb").get_renderer()
