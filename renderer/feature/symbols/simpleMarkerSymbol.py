import arcpy

from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface, convert_int_to_rgb_string
import copy
from dictionaries.singleSymbol import SingleSymbol


class SimpleMarkerSymbol:

    def __init__(self):
        pass

    @staticmethod
    def create_simple_marker_symbol(i_symbol):
        """ This collects all properties of a simple marker symbol and returns a dictionary of them

        :param i_symbol: the symbol to investigate
        :return: symbol_properties as dictionary
        """
        marker_dict = copy.deepcopy(SingleSymbol.propDict)
        symbol_properties = {'simpleSymbolClass': "SimpleMarker", 'dict_symbols': marker_dict}

        symbol_marker = change_interface(i_symbol, ArcGisModules.module_display.IMarkerSymbol)

        try:
            multilayer_symbol = change_interface(
                i_symbol,
                ArcGisModules.module_display.IMultiLayerMarkerSymbol).Layer[0]
            symbol_simple_marker = change_interface(multilayer_symbol, ArcGisModules.module_display.ISimpleMarkerSymbol)
        except AttributeError:
            symbol_simple_marker = change_interface(i_symbol, ArcGisModules.module_display.ISimpleMarkerSymbol)

        if symbol_simple_marker:
            symbol_properties['dict_symbols']['style'] = symbol_simple_marker.Style
            symbol_properties['dict_symbols']['name'] = SingleSymbol.simple_marker_style_dict[
                symbol_simple_marker.Style]
            if symbol_simple_marker.Outline:
                symbol_properties['dict_symbols']['outline_style'] = "solid"
                symbol_properties['dict_symbols']['outline_color'] = convert_int_to_rgb_string(symbol_simple_marker.OutlineColor.RGB)
                symbol_properties['dict_symbols']['outline_width'] = symbol_simple_marker.OutlineSize
            else:
                symbol_properties['dict_symbols']['outline_style'] = "no"
            symbol_properties['dict_symbols']['offset'] = str(symbol_simple_marker.XOffset) + "," + str(
                symbol_simple_marker.YOffset)

        symbol_properties['dict_symbols']['angle'] = symbol_marker.Angle
        try:
            layer_color = convert_int_to_rgb_string(symbol_marker.Color.RGB)
            if symbol_marker.Color.NullColor:
                symbol_properties['dict_symbols']['style'] = "no"
        except ValueError:
            layer_color = '0,0,0,255'
            arcpy.AddWarning("\t\tThere was an Error coloring the Layer. Default Color is black.")

        symbol_properties['dict_symbols']['color'] = layer_color

        symbol_properties['dict_symbols']['size'] = symbol_marker.Size

        return symbol_properties
