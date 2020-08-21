from dictionaries.singleSymbol import SingleSymbol


class SimpleLine:
    def __init__(self):
        pass

    @staticmethod
    def create_simple_line(symbol_simple_line, symbol_properties):
        """ This collects all properties of a simple-line symbol and writes it in the symbol properties

        :param symbol_simple_line: the cartographic-line symbol
        :param symbol_properties: the belonging properties dictionary
        """
        symbol_properties['dict_symbols']['line_style'] = \
            SingleSymbol.simple_line_style_dict[symbol_simple_line.Style]
