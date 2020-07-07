import arcpy

from dictionaries.singleSymbol import SingleSymbol
from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_arc_object, unpack2rgb
import copy


class FeatureSimpleFillSymbol:

    def __init__(self):
        pass

    @staticmethod
    def create_feature_simple_fill_symbol(i_symbol):
        """ This collects all properties of a simple fill symbol and returns a dictionary of them

        :param i_symbol: the symbol to investigate
        :return: the symbol_properties as dictionary
        """
        fill_dict = copy.deepcopy(SingleSymbol.propDict)
        symbol_properties = {'simpleSymbolClass': "SimpleFill", 'dict_symbols': fill_dict}

        fill_symbol = type_cast_arc_object(i_symbol, ArcGisModules.module_display.IFillSymbol)

        try:
            layer_color = unpack2rgb(fill_symbol.Color.RGB)
            if fill_symbol.Color.NullColor:
                symbol_properties['dict_symbols']['style'] = "no"
            else:
                symbol_properties['dict_symbols']['style'] = "solid"
        except ValueError:
            layer_color = '0,0,0,255'
            symbol_properties['dict_symbols']['style'] = "solid"
            arcpy.AddWarning(
                "\t\tError occured while render color. Default Color is black. Default style is solid."
            )

        symbol_properties['dict_symbols']['color'] = layer_color

        if fill_symbol.Outline:
            simple_outline = type_cast_arc_object(fill_symbol.Outline, ArcGisModules.module_display.ISimpleLineSymbol)
            if simple_outline:
                symbol_properties['dict_symbols']['outline_style'] = \
                    SingleSymbol.simple_line_style_dict[simple_outline.Style]
            symbol_properties['dict_symbols']['outline_color'] = unpack2rgb(fill_symbol.Outline.Color.RGB)
            symbol_properties['dict_symbols']['outline_width'] = fill_symbol.Outline.Width

        return symbol_properties
