from renderer.renderer import Renderer as rendererObj


class RasterLayer:
    def __init__(self):
        pass

    @staticmethod
    def create_raster_layer_content(base, map_layer_element):
        """ This Function creates raster-layer specific content in the
            fitting maplayer-element

        :param base: Is the self from the LayerObject
        :param map_layer_element: the maplayer_element in the DOM
        """
        map_layer_element.setAttribute("type", "raster")

        for datasource, provider in zip(map_layer_element.getElementsByTagName('datasource'),
                                        map_layer_element.getElementsByTagName('provider')):
            provider.appendChild(base.document.createTextNode("gdal"))
            datasource.appendChild(base.document.createTextNode(str(base.layer.dataSource)))

        rendererObj(base.document, map_layer_element, base.arc_layer, base.layer, "raster").get_renderer()
