class SubSymbolProvider:
    def __init__(self):
        pass

    @staticmethod
    def create_sub_symbol(symbol_properties, symbol_type):
        """ This  creates a layer for a subsymbol in the symbol properties of a "parent" symbol

        :param symbol_properties: the symbol-properties of the parent symbol
        :param symbol_type: the type of the subsymbol
        """
        symbol_properties['subSymbol'] = {
            'name': '@0@0',
            'force_rhr': '0',
            'alpha': '1',
            'clip_to_extent': '1',
            'symbol_type': symbol_type,
            'layer': [],
        }
