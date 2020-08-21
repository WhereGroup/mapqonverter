from renderer.feature.symbols.subSymbolProvider import SubSymbolProvider
from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider


class HashLine:
    def __init__(self):
        pass

    @staticmethod
    def create_hash_line(symbol_hash_line, symbol_properties):
        """ This collects all properties of a hash-line symbol and writes it in the symbol properties

        :param symbol_hash_line: the hash symbol
        :param symbol_properties: the belonging properties dictionary
        """
        symbol_properties['simpleSymbolClass'] = "HashLine"
        hash_angle = symbol_hash_line.Angle + 90
        if hash_angle > 360:
            hash_angle = hash_angle - 360
        symbol_properties['dict_symbols']['hash_angle'] = str(hash_angle * -1)
        symbol_properties['dict_symbols']['hash_length'] = str(symbol_hash_line.Width)
        symbol_properties['dict_symbols']['hash_length_unit'] = "Point"
        SubSymbolProvider.create_sub_symbol(symbol_properties, 'line')

        SymbolPropertiesProvider.get_line_properties(
            symbol_properties['subSymbol'],
            symbol_hash_line.HashSymbol
        )
