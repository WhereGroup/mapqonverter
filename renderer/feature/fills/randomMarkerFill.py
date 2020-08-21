from modules.functions import convert_int_to_rgb_string
import copy
from dictionaries.singleSymbol import SingleSymbol
from renderer.feature.symbols.subSymbolProvider import SubSymbolProvider


class RandomMarkerFillSymbol:

    def __init__(self):
        pass

    @staticmethod
    def create_feature_marker_fill_symbol(i_symbol):
        """ This collects all properties of a marker fill symbol and returns a dictionary of them

        :param i_symbol: the symbol to investigate
        :return: symbol_properties as dictionary
        """
        fill_dict = copy.deepcopy(SingleSymbol.propDict)
        symbol_properties = {
            'simpleSymbolClass': "RandomMarkerFill",
            'dict_symbols': fill_dict,
        }
        layer_color = convert_int_to_rgb_string(i_symbol.MarkerSymbol.Color.RGB)
        symbol_properties['dict_symbols']['color'] = layer_color
        symbol_properties['dict_symbols']['clip_points'] = '1'
        symbol_properties['dict_symbols']['count_method'] = '1'
        symbol_properties['dict_symbols']['density_area'] = '250'
        symbol_properties['dict_symbols']['density_area_unit'] = 'MM'
        symbol_properties['dict_symbols']['density_area_scale'] = '3x:0,0,0,0,0,0'
        symbol_properties['dict_symbols']['point_count'] = '10'
        symbol_properties['dict_symbols']['seed'] = '48648189'

        SubSymbolProvider.create_sub_symbol(symbol_properties, 'marker')

        from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider
        SymbolPropertiesProvider.get_point_properties(
            symbol_properties['subSymbol'],
            i_symbol.MarkerSymbol
        )

        return symbol_properties
