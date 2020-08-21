class SimpleSymbol:

    def __init__(self):
        pass

    @staticmethod
    def create_simple_symbol(xml_document, symbols_element, properties, count, alpha):
        """ This write all properties of a simple symbol in the symbol_element in the DOM

        :param xml_document: is the DOM
        :param symbols_element: the symbols-element in the DOM
        :param properties: the symbol properties as dictionary
        :param count: the number of the symbol (just interesting for the naming)
        :param alpha: the transparency level
        """
        symbol_element = xml_document.createElement("symbol")
        symbol_element.setAttribute("alpha", alpha)
        symbol_element.setAttribute("clip_to_extent", "1")
        symbol_element.setAttribute("type", properties['symbol_type'])
        symbol_element.setAttribute("name", str(count))
        symbols_element.appendChild(symbol_element)

        for layer in reversed(properties['layer']):
            renderer_layer_element = xml_document.createElement("layer")
            renderer_layer_element.setAttribute("pass", "0")
            renderer_layer_element.setAttribute("enabled", "1")
            renderer_layer_element.setAttribute("locked", "0")
            renderer_layer_element.setAttribute("class", layer['simpleSymbolClass'])
            symbol_element.appendChild(renderer_layer_element)

            for key, value in layer['dict_symbols'].items():

                symbol_properties_element = xml_document.createElement("prop")
                symbol_properties_element.setAttribute("k", unicode(key))
                symbol_properties_element.setAttribute("v", unicode(value))
                renderer_layer_element.appendChild(symbol_properties_element)

            data_defined_properties_element = xml_document.createElement("data_defined_properties")
            renderer_layer_element.appendChild(data_defined_properties_element)

            data_defined_option_element = xml_document.createElement("Option")
            data_defined_option_element.setAttribute("type", "Map")
            data_defined_properties_element.appendChild(data_defined_option_element)

            data_defined_option_value_element = xml_document.createElement("Option")
            data_defined_option_value_element.setAttribute("value", "")
            data_defined_option_value_element.setAttribute("type", "QString")
            data_defined_option_value_element.setAttribute("name", "name")
            data_defined_option_element.appendChild(data_defined_option_value_element)

            data_defined_option_name_element = xml_document.createElement("Option")
            data_defined_option_name_element.setAttribute("name", "properties")
            data_defined_option_element.appendChild(data_defined_option_name_element)

            data_defined_option_collection_element = xml_document.createElement("Option")
            data_defined_option_collection_element.setAttribute("value", "collection")
            data_defined_option_collection_element.setAttribute("type", "QString")
            data_defined_option_collection_element.setAttribute("name", "type")
            data_defined_option_element.appendChild(data_defined_option_collection_element)

            if 'subSymbol' in layer:
                SimpleSymbol.create_simple_symbol(xml_document, renderer_layer_element, layer['subSymbol'], "@0@0", '1')



