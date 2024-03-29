import random

import arcpy
from comtypes.client import CreateObject

from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface, convert_int_to_rgb_string
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

        layer_color = convert_int_to_rgb_string(i_symbol.Color.RGB)
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

        symbol_properties['dict_symbols']['outline_color'] = str(convert_int_to_rgb_string(i_symbol.Outline.Color.RGB))
        symbol_properties['dict_symbols']['outline_width'] = str(i_symbol.Outline.Width)

        FeatureGradientFillSymbol.create_color_ramp_properties(i_symbol.ColorRamp, radial_fill, symbol_properties)

        return symbol_properties

    @staticmethod
    def get_colors_from_ramp(ramp):
        """ this returns a list of the used colors of a color-ramp

        :param ramp: the ramp you want to investigate
        :return: a list of colors
        """
        colors = []
        algorithmic_color_map = change_interface(ramp, ArcGisModules.module_display.IAlgorithmicColorRamp)
        preset_color_ramp = change_interface(ramp, ArcGisModules.module_display.IPresetColorRamp)
        random_color_ramp = change_interface(ramp, ArcGisModules.module_display.IRandomColorRamp)
        if algorithmic_color_map:
            colors.append(algorithmic_color_map.FromColor)
            colors.append(algorithmic_color_map.ToColor)
        elif preset_color_ramp:
            for colorNumber in range(preset_color_ramp.NumberOfPresetColors):
                colors.append(preset_color_ramp.PresetColor[colorNumber])
        elif random_color_ramp:
            for color in range(0, 13):
                hsv_color_object = CreateObject(ArcGisModules.module_display.HsvColor,
                                                interface=ArcGisModules.module_display.IHsvColor)

                if random_color_ramp.StartHue > random_color_ramp.EndHue:
                    random_hue1 = random.randint(0, random_color_ramp.EndHue)
                    random_hue2 = random.randint(random_color_ramp.StartHue, 360)
                    random_hue = random.choice([random_hue1, random_hue2])
                else:
                    random_hue = random.randint(random_color_ramp.StartHue, random_color_ramp.EndHue)

                hsv_color_object.Hue = random_hue
                random_saturation = random.randint(random_color_ramp.MinSaturation, random_color_ramp.MaxSaturation)
                hsv_color_object.Saturation = random_saturation
                random_value = random.randint(random_color_ramp.MinValue, random_color_ramp.MaxValue)
                hsv_color_object.Value = random_value

                colors.append(hsv_color_object)
        else:
            for colorNumber in range(ramp.Size):
                colors.append(ramp.Color[colorNumber])

        if len(colors) == 0:
            rgb_color_object_1 = CreateObject(ArcGisModules.module_display.RgbColor,
                                              interface=ArcGisModules.module_display.IColor)
            rgb_color_object_1.RGB = 16777215
            colors.append(rgb_color_object_1)

            rgb_color_object_2 = CreateObject(ArcGisModules.module_display.RgbColor,
                                              interface=ArcGisModules.module_display.IColor)
            rgb_color_object_2.RGB = 0
            colors.append(rgb_color_object_2)

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
                    symbol_properties['dict_symbols']['color1'] = convert_int_to_rgb_string(color.RGB)
                if color == colors[-1] and ramp_number == 1:
                    symbol_properties['dict_symbols']['color2'] = convert_int_to_rgb_string(color.RGB)
            else:
                if color == colors[0] and ramp_number == 1:
                    symbol_properties['dict_symbols']['color1'] = convert_int_to_rgb_string(color.RGB)
                if color == colors[-1] and ramp_number == multi_gradient_fill.NumberOfRamps:
                    symbol_properties['dict_symbols']['color2'] = convert_int_to_rgb_string(color.RGB)

            symbol_properties['dict_symbols']['stops'] += "{};{}:".format(color_range,
                                                                          convert_int_to_rgb_string(color.RGB)
                                                                          )

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
    def write_solo_gradient_colors_in_dict(color_ramp, radial_fill, symbol_properties):
        """This writes the the color-range of the used color-ramp of a multi_gradient_fill_symbol

        :param color_ramp: The Color Ramp Symbol
        :param radial_fill: This declares if the gradient has a radial fill - boolean
        :param symbol_properties: symbol_properties as dictionary
        """
        colors = FeatureGradientFillSymbol.get_colors_from_ramp(color_ramp)
        first_color = convert_int_to_rgb_string(colors[0].RGB)
        second_color = convert_int_to_rgb_string(colors[1].RGB)

        color1 = first_color
        color2 = second_color
        if radial_fill:
            color1 = second_color
            color2 = first_color

        symbol_properties['dict_symbols']['color'] = color1
        symbol_properties['dict_symbols']['color1'] = color1
        symbol_properties['dict_symbols']['color2'] = color2
        symbol_properties['dict_symbols']['gradient_color2'] = color2

        random_color_ramp = change_interface(color_ramp, ArcGisModules.module_display.IRandomColorRamp)
        if random_color_ramp:
            symbol_properties['dict_symbols']['discrete'] = "1"
        else:
            symbol_properties['dict_symbols']['color_type'] = "0"
        color_range = 0.0
        if color_ramp.Size == 0 and not random_color_ramp:
            step_size = 0.5
        else:
            step_size = 1.0 / len(colors)
        if radial_fill:
            colors.reverse()
        for colorNumber, color in enumerate(colors):
            symbol_properties['dict_symbols']['stops'] += "{};{}".format(color_range,
                                                                         convert_int_to_rgb_string(color.RGB)
                                                                         )
            if colorNumber != len(colors):
                symbol_properties['dict_symbols']['stops'] += ":"
            color_range += step_size

    @staticmethod
    def create_color_ramp_properties(color_ramp, radial_fill, symbol_properties):
        """ This add the properties of the color ramp to a dictionary and returns it

        :param color_ramp: The Color Ramp Symbol
        :param radial_fill: This declares if the gradient has a radial fill - boolean
        :param symbol_properties: symbol_properties as dictionary
        :return: adapted symbol properties
        """
        multi_gradient_fill = change_interface(color_ramp, ArcGisModules.module_display.IMultiPartColorRamp)

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
                color_ramp,
                radial_fill,
                symbol_properties
            )
        return symbol_properties
