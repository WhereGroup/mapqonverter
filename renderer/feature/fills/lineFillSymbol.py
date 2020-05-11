from modules.snippets102 import unpack2rgb
import copy
from dictionaries.singleSymbol import SingleSymbol
from renderer.feature.symbols.subSymbolProvider import SubSymbolProvider


class FeatureLineFillSymbol:

    def __init__(self):
        pass

    @staticmethod
    def create_feature_line_fill_symbol(i_symbol):
        """ This collects all properties of a line fill symbol and returns a dictionary of them

        :param i_symbol: the symbol to investigate
        :return: symbol_properties as dictionary
        """
        fill_dict = copy.deepcopy(SingleSymbol.propDict)
        symbol_properties = {
            'simpleSymbolClass': "LinePatternFill",
            'dict_symbols': fill_dict,
        }

        symbol_properties['dict_symbols']['angle'] = i_symbol.Angle
        layer_color = unpack2rgb(i_symbol.LineSymbol.Color.RGB)
        symbol_properties['dict_symbols']['color'] = layer_color
        symbol_properties['dict_symbols']['offset'] = i_symbol.Offset
        symbol_properties['dict_symbols']['distance'] = str(i_symbol.Separation)

        symbol_properties['dict_symbols']['outline_color'] = unpack2rgb(i_symbol.Outline.Color.RGB)
        symbol_properties['dict_symbols']['outline_width'] = i_symbol.Outline.Width

        SubSymbolProvider.create_sub_symbol(symbol_properties, 'line')

        from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider
        SymbolPropertiesProvider.get_line_properties(
            symbol_properties['subSymbol'],
            i_symbol.LineSymbol
        )

        return symbol_properties
