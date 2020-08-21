from dictionaries.singleSymbol import SingleSymbol


class CartographicLine:

    def __init__(self):
        pass

    @staticmethod
    def create_cartographic_line(symbol_cartographic_line, symbol_properties):
        """ This collects all properties of a cartographic-line symbol and writes it in the symbol properties

        :param symbol_cartographic_line: the cartographic-line symbol
        :param symbol_properties: the belonging properties dictionary
        """
        symbol_properties['dict_symbols']['capstyle'] = \
            SingleSymbol.line_cap_style_dict[symbol_cartographic_line.Cap]

        symbol_properties['dict_symbols']['joinstyle'] = \
            SingleSymbol.line_join_style_dict[symbol_cartographic_line.Join]
