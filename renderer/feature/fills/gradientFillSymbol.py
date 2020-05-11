import arcpy

from modules.arcGisModules import ArcGisModules
from modules.snippets102 import type_cast_module, unpack2rgb
import copy
from dictionaries.singleSymbol import SingleSymbol


class FeatureGradientFillSymbol:

    def __init__(self):
        pass

    @staticmethod
    def create_feature_gradient_fill_symbol(i_symbol):
        """ This collects all properties of a gradient fill symbol and returns a dictionary of them

        :param i_symbol: the symbol to investigate
        :return: symbol_properties as dictionary
        """
        fill_dict = copy.deepcopy(SingleSymbol.propDict)
        symbol_properties = {
            'simpleSymbolClass': "GradientFill",
            'dict_symbols': fill_dict,
        }

        layer_color = unpack2rgb(i_symbol.Color.RGB)
        symbol_properties['dict_symbols']['color'] = layer_color

        angle = i_symbol.GradientAngle + 270.0
        if angle >= 360:
            symbol_properties['dict_symbols']['angle'] = str(angle - 360)
        else:
            symbol_properties['dict_symbols']['angle'] = str(angle)

        symbol_properties['dict_symbols']['type'] = SingleSymbol.gradient_style[i_symbol.Style]
        if i_symbol.Style == 1 | i_symbol.Style == 3:
            arcpy.AddWarning("Rectangular and buffered gradient is not supported by QGIS")

        radial_fill = False

        if symbol_properties['dict_symbols']['type'] == "1":
            symbol_properties['dict_symbols']["reference_point1_iscentroid"] = "1"
            symbol_properties['dict_symbols']["reference_point2"] = "1,1"
            radial_fill = True  # QGIS radial_fill works in the other direction of the ColorRamp

        symbol_properties['dict_symbols']['rampType'] = "gradient"
        symbol_properties['dict_symbols']['discrete'] = "0"
        symbol_properties['dict_symbols']['spread'] = "0"

        symbol_properties['dict_symbols']['outline_color'] = str(unpack2rgb(i_symbol.Outline.Color.RGB))
        symbol_properties['dict_symbols']['outline_width'] = str(i_symbol.Outline.Width)

        multi_gradient_fill = type_cast_module(i_symbol.ColorRamp, ArcGisModules.module_display.IMultiPartColorRamp)

        symbol_properties['dict_symbols']['stops'] = ""

        if multi_gradient_fill:

            if radial_fill:
                number_of_ramps = reversed(range(1, multi_gradient_fill.NumberOfRamps + 1))
            else:
                number_of_ramps = range(1, multi_gradient_fill.NumberOfRamps + 1)
            color_range = 0.0
            for ramp in number_of_ramps:
                color_range_temp = FeatureGradientFillSymbol.write_multi_gradient_colors_in_dict(
                    multi_gradient_fill,
                    ramp,
                    color_range,
                    radial_fill,
                    symbol_properties,
                )

                color_range = color_range_temp

            symbol_properties['dict_symbols']['color_type'] = "1"

        else:
            FeatureGradientFillSymbol.write_solo_gradient_colors_in_dict(
                i_symbol,
                radial_fill,
                symbol_properties
            )

        return symbol_properties

    @staticmethod
    def get_colors_from_ramp(ramp):
        """ this returns a list of the used colors of a color-ramp

        :param ramp: the ramp you want to investigate
        :return: a list of colors
        """
        colors = []
        algorithmic_color_map = type_cast_module(ramp, ArcGisModules.module_display.IAlgorithmicColorRamp)
        preset_color_ramp = type_cast_module(ramp, ArcGisModules.module_display.IPresetColorRamp)
        if algorithmic_color_map:
            colors.append(algorithmic_color_map.FromColor)
            colors.append(algorithmic_color_map.ToColor)
        elif preset_color_ramp:
            print preset_color_ramp.NumberOfPresetColors
            for colorNumber in range(preset_color_ramp.NumberOfPresetColors):
                colors.append(preset_color_ramp.PresetColor[colorNumber])
        else:
            for colorNumber in range(ramp.Size):
                colors.append(ramp.Color[colorNumber])

        return colors

    @staticmethod
    def write_multi_gradient_colors_in_dict(multi_gradient_fill, ramp_number, color_range, radial_fill,
                                            symbol_properties):
        """ This returns the the color-range of the used color-ramp (and adds it to the existing range)
            of a multi_gradient_fill_symbol

        :param multi_gradient_fill: Is the multi_gradient_fill symbol
        :param ramp_number: the index number of the color-ramp
        :param color_range: the existing color_range
        :param radial_fill: This declares if the gradient has a radial fill
        :param symbol_properties: symbol_properties as dictionary
        :return: the actual color_range of a ramp
        """
        colors = FeatureGradientFillSymbol.get_colors_from_ramp(multi_gradient_fill.Ramp[ramp_number-1])
        color_range_for_ramp = 1.0 / multi_gradient_fill.NumberOfRamps

        if len(colors) == 2:
            step_size = color_range_for_ramp
        else:
            step_size = color_range_for_ramp / len(colors)

        if radial_fill:
            colors.reverse()

        for color in colors:
            if radial_fill:
                if color == colors[0] and ramp_number == multi_gradient_fill.NumberOfRamps:
                    symbol_properties['dict_symbols']['color1'] = unpack2rgb(color.RGB)
                if color == colors[-1] and ramp_number == 1:
                    symbol_properties['dict_symbols']['color2'] = unpack2rgb(color.RGB)
            else:
                if color == colors[0] and ramp_number == 1:
                    symbol_properties['dict_symbols']['color1'] = unpack2rgb(color.RGB)
                if color == colors[-1] and ramp_number == multi_gradient_fill.NumberOfRamps:
                    symbol_properties['dict_symbols']['color2'] = unpack2rgb(color.RGB)

            symbol_properties['dict_symbols']['stops'] += "{};{}:".format(color_range, unpack2rgb(color.RGB))

            if color in colors[:-1]:
                color_range += step_size
            else:
                # This is hacky stuff to support hard borders between multiple ColorRamps O_o
                # If element is last element of a colorRamp make short step after it to have a hard border to the next.
                # No Step after last element of last colorRamp as well
                if ramp_number != multi_gradient_fill.NumberOfRamps or radial_fill and ramp_number != 1:
                    color_range += 0.01

        return color_range

    @staticmethod
    def write_solo_gradient_colors_in_dict(i_symbol, radial_fill, symbol_properties):
        """This writes the the color-range of the used color-ramp of a multi_gradient_fill_symbol

        :param i_symbol: The used Fill Symbol
        :param radial_fill: This declares if the gradient has a radial fill
        :param symbol_properties: symbol_properties as dictionary
        """
        colors = FeatureGradientFillSymbol.get_colors_from_ramp(i_symbol.ColorRamp)
        first_color = unpack2rgb(colors[0].RGB)
        second_color = unpack2rgb(colors[1].RGB)

        color1 = first_color
        color2 = second_color
        if radial_fill:
            color1 = second_color
            color2 = first_color

        symbol_properties['dict_symbols']['color'] = color1
        symbol_properties['dict_symbols']['color1'] = color1
        symbol_properties['dict_symbols']['color2'] = color2
        symbol_properties['dict_symbols']['gradient_color2'] = color2
        symbol_properties['dict_symbols']['color_type'] = "0"
        color_range = 0.0
        if i_symbol.ColorRamp.Size == 0:
            step_size = 0.5
        else:
            step_size = 1.0 / len(colors)
        if radial_fill:
            colors.reverse()
        for colorNumber, color in enumerate(colors):
            symbol_properties['dict_symbols']['stops'] += "{};{}".format(color_range, unpack2rgb(color.RGB))
            if colorNumber != len(colors):
                symbol_properties['dict_symbols']['stops'] += ":"
            color_range += step_size
