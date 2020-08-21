import copy

from dictionaries.singleSymbol import SingleSymbol
from modules.functions import convert_int_to_rgb_string


class CharacterMarkerSymbol:
    def __init__(self):
        pass

    @staticmethod
    def create_character_marker_symbol(character_symbol):
        marker_dict = copy.deepcopy(SingleSymbol.propDict)
        symbol_properties = {'simpleSymbolClass': "FontMarker", 'dict_symbols': marker_dict}

        font = character_symbol.Font.Name
        character = unichr(character_symbol.CharacterIndex)

        symbol_properties['dict_symbols']['font'] = font
        symbol_properties['dict_symbols']['chr'] = character
        symbol_properties['dict_symbols']['angle'] = character_symbol.Angle * -1
        symbol_properties['dict_symbols']['size'] = character_symbol.Size
        symbol_properties['dict_symbols']['offset'] = '{},{}'.format(character_symbol.XOffset,
            character_symbol.YOffset)

        symbol_properties['dict_symbols']['color'] = convert_int_to_rgb_string(character_symbol.Color.RGB)

        return symbol_properties
