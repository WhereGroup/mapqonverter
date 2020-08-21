class NullRenderer:
    def __init__(self):
        pass

    @staticmethod
    def create_null_symbol_renderer(base):
        """ This creates the smallest possible renderer in the DOM

        :param base: the renderer object
        """
        renderer_element = base.xml_document.createElement("renderer-v2")
        renderer_element.setAttribute("type", "nullSymbol")
        base.map_layer_element.appendChild(renderer_element)
