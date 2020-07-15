import arcpy

from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_arc_object, convert_int_to_rgb_string
import copy
from dictionaries.singleSymbol import SingleSymbol
from renderer.feature.lines.hashLine import HashLine
from renderer.feature.lines.cartographicLine import CartographicLine
from renderer.feature.lines.markerLine import MarkerLine
from renderer.feature.lines.simpleLine import SimpleLine


class LineSymbol:

    def __init__(self):
        pass

    dict_line_creation = {
        'hash': HashLine.create_hash_line,
        'marker': MarkerLine.create_symbol_marker_line,
        'cartographic': CartographicLine.create_cartographic_line,
        'simple': SimpleLine.create_simple_line
    }

    @staticmethod
    def get_line_symbol_types(i_symbol):
        """ This function detects the type of line symbol and returns it

        :param i_symbol: the symbol to investigate
        :return: the line type and fitting ArcObject-Symbol as dictionary
        """
        line_symbol_type = {}
        symbol_hash_line = type_cast_arc_object(i_symbol, ArcGisModules.module_display.IHashLineSymbol)
        symbol_marker_line = type_cast_arc_object(i_symbol, ArcGisModules.module_display.IMarkerLineSymbol)
        symbol_cartographic_line = type_cast_arc_object(i_symbol, ArcGisModules.module_display.ICartographicLineSymbol)
        symbol_simple_line = type_cast_arc_object(i_symbol, ArcGisModules.module_display.ISimpleLineSymbol)

        if symbol_hash_line:
            line_symbol_type["hash"] = symbol_hash_line
        elif symbol_marker_line:
            line_symbol_type["marker"] = symbol_marker_line
        elif symbol_cartographic_line:
            line_symbol_type["cartographic"] = symbol_cartographic_line
        elif symbol_simple_line:
            line_symbol_type["simple"] = symbol_simple_line
        else:
            pass

        return line_symbol_type

    @staticmethod
    def create_feature_line_symbol(i_symbol):
        """ This collects all properties of a line symbol and returns a dictionary of them

        :param i_symbol: the symbol to investigate
        :return: the symbol_properties as dictionary
        """
        line_dict = copy.deepcopy(SingleSymbol.propDict)
        symbol_properties = {
            'simpleSymbolClass': "SimpleLine",
            'dict_symbols': line_dict,
        }

        line_symbol_types = LineSymbol.get_line_symbol_types(i_symbol)

        for line_type, line_symbol in line_symbol_types.items():
            LineSymbol.dict_line_creation[line_type](line_symbol, symbol_properties)

        LineSymbol.create_line_properties(i_symbol, symbol_properties)

        basic_line_symbol = type_cast_arc_object(i_symbol, ArcGisModules.module_display.ILineSymbol)
        try:
            layer_color = convert_int_to_rgb_string(basic_line_symbol.Color.RGB)
        except ValueError:
            symbol_properties['dict_symbols']['line_style'] = 'no'
            layer_color = '0,0,0,255'
            arcpy.AddWarning(
                "\t\tError occured while rendering color. Default color is none."
            )
        symbol_properties['dict_symbols']['line_color'] = layer_color
        symbol_properties['dict_symbols']['line_width'] = basic_line_symbol.Width

        return symbol_properties

    @staticmethod
    def create_line_properties(line_symbol, symbol_properties):
        """ This function writes the existing line properties in the symbol_properties dictionary

        :param line_symbol: the line_symbol to investigate
        :param symbol_properties: the properties of the line as dictionary
        """
        line_properties = type_cast_arc_object(line_symbol, ArcGisModules.module_display.ILineProperties)
        if line_properties:
            if line_properties.Template:
                pattern_count = line_properties.Template.PatternElementCount
                width_counter = 0
                custom_dash = ''
                for pattern_element_index in range(0, pattern_count):
                    pattern_element = line_properties.Template.GetPatternElement(pattern_element_index)
                    if pattern_element_index > 0:
                        custom_dash += ';'
                    custom_dash += '{};{}'.format(pattern_element[0], pattern_element[1])
                    width_counter += pattern_element[0] + pattern_element[1]
                symbol_properties['dict_symbols']['customdash'] = custom_dash
                symbol_properties['dict_symbols']['use_custom_dash'] = '1'
                symbol_properties['dict_symbols']['interval'] = str(width_counter * line_properties.Template.Interval)
            symbol_properties['dict_symbols']['interval_unit'] = 'Point'

            symbol_properties['dict_symbols']['offset'] = str(line_properties.Offset * -1)
