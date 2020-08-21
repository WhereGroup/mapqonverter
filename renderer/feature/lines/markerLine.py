from renderer.feature.symbols.subSymbolProvider import SubSymbolProvider
from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider


class MarkerLine:
    def __init__(self):
        pass

    @staticmethod
    def create_symbol_marker_line(symbol_marker_line, symbol_properties):
        """ This collects all properties of a marker-line symbol and writes it in the symbol properties

        :param symbol_marker_line: the marker-line symbol
        :param symbol_properties: the belonging properties dictionary
        """
        symbol_properties['simpleSymbolClass'] = "MarkerLine"
        SubSymbolProvider.create_sub_symbol(symbol_properties, 'marker')

        SymbolPropertiesProvider.get_point_properties(
            symbol_properties['subSymbol'],
            symbol_marker_line.MarkerSymbol
        )
