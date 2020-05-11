class WMSRenderer:
    def __init__(self):
        pass

    @staticmethod
    def adapt_wms_renderer(raster_renderer_element):
        """ This sets the attributes of a renderer WMS specific

        :param raster_renderer_element: the renderer element in the DOM
        """
        raster_renderer_element.setAttribute("type", "singlebandcolordata")
        raster_renderer_element.setAttribute("band", "1")
