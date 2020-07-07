from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_arc_object, convert_int_to_rgb_string
import copy
from dictionaries.singleSymbol import SingleSymbol
from renderer.feature.symbols.subSymbolProvider import SubSymbolProvider


class FeatureMarkerFillSymbol:

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
            'simpleSymbolClass': "PointPatternFill",
            'dict_symbols': fill_dict,
        }
        layer_color = convert_int_to_rgb_string(i_symbol.MarkerSymbol.Color.RGB)
        symbol_properties['dict_symbols']['color'] = layer_color

        fill_properties = type_cast_arc_object(i_symbol, ArcGisModules.module_display.IFillProperties)

        symbol_properties['dict_symbols']['displacement_x'] = str(fill_properties.XOffset)
        symbol_properties['dict_symbols']['displacement_y'] = str(fill_properties.YOffset)
        symbol_properties['dict_symbols']['displacement_x_unit'] = "Pixel"
        symbol_properties['dict_symbols']['displacement_y_unit'] = "Pixel"

        symbol_properties['dict_symbols']['distance_x'] = str(fill_properties.XSeparation)
        symbol_properties['dict_symbols']['distance_y'] = str(fill_properties.YSeparation)
        symbol_properties['dict_symbols']['distance_x_unit'] = "Pixel"
        symbol_properties['dict_symbols']['distance_y_unit'] = "Pixel"

        symbol_properties['dict_symbols']['outline_color'] = str(convert_int_to_rgb_string(i_symbol.Outline.Color.RGB))
        symbol_properties['dict_symbols']['outline_width'] = str(i_symbol.Outline.Width)

        SubSymbolProvider.create_sub_symbol(symbol_properties, 'marker')

        from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider
        SymbolPropertiesProvider.get_point_properties(
            symbol_properties['subSymbol'],
            i_symbol.MarkerSymbol
        )

        return symbol_properties
