from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_arc_object
from renderer.feature.fills.gradientFillSymbol import FeatureGradientFillSymbol
from renderer.feature.fills.lineFillSymbol import FeatureLineFillSymbol
from renderer.feature.fills.markerFillSymbol import FeatureMarkerFillSymbol
from renderer.feature.fills.simpleFillSymbol import FeatureSimpleFillSymbol
from renderer.feature.symbols.simpleMarkerSymbol import SimpleMarkerSymbol


class SymbolPropertiesProvider:
    def __init__(self):
        pass
    
    @staticmethod
    def get_polygon_properties(symbol_properties, i_symbol):
        """ This function collects all properties of the polygon symbol

        :param symbol_properties: This is a dictionary for the properties of a symbol
        :param i_symbol: this is the used polygon symbol
        """
        symbol_properties['symbol_type'] = "fill"
        symbol_properties['layer'] = []
        multilayer_symbol = type_cast_arc_object(i_symbol, ArcGisModules.module_display.IMultiLayerFillSymbol)

        if multilayer_symbol:
            symbol_collection = SymbolPropertiesProvider.get_multilayer_symbol_collection(multilayer_symbol)

            for symbol in symbol_collection:
                line_fill_symbol = type_cast_arc_object(symbol, ArcGisModules.module_display.ILineFillSymbol)
                marker_fill_symbol = type_cast_arc_object(symbol, ArcGisModules.module_display.IMarkerFillSymbol)
                gradient_fill_symbol = type_cast_arc_object(symbol, ArcGisModules.module_display.IGradientFillSymbol)

                outline = type_cast_arc_object(symbol.Outline, ArcGisModules.module_display.ILineSymbol)

                if outline:
                    SymbolPropertiesProvider.get_multilayer_line_symbol(outline, symbol_properties)
                if line_fill_symbol:
                    symbol_properties['layer'].append(
                        FeatureLineFillSymbol.create_feature_line_fill_symbol(line_fill_symbol)
                    )
                elif marker_fill_symbol:
                    symbol_properties['layer'].append(
                        FeatureMarkerFillSymbol.create_feature_marker_fill_symbol(marker_fill_symbol)
                    )
                elif gradient_fill_symbol:
                    symbol_properties['layer'].append(
                        FeatureGradientFillSymbol.create_feature_gradient_fill_symbol(gradient_fill_symbol)
                    )
                else:
                    symbol_properties['layer'].append(FeatureSimpleFillSymbol.create_feature_simple_fill_symbol(symbol))

        else:
            symbol_properties['layer'].append(FeatureSimpleFillSymbol.create_feature_simple_fill_symbol(i_symbol))

    @staticmethod
    def get_line_properties(symbol_properties, i_symbol):
        """ This function collects all properties of the line symbol

        :param symbol_properties: This is a dictionary for the properties of a symbol
        :param i_symbol: this is the used polygon symbol
        """
        symbol_properties['symbol_type'] = "line"
        symbol_properties['layer'] = []

        SymbolPropertiesProvider.get_multilayer_line_symbol(i_symbol, symbol_properties)

    @staticmethod
    def get_multilayer_line_symbol(i_symbol, symbol_properties):
        """ This function collects all properties of the multiline symbol

        :param symbol_properties: This is a dictionary for the properties of a symbol
        :param i_symbol: this is the used polygon symbol
        """
        multilayer_symbol = type_cast_arc_object(i_symbol, ArcGisModules.module_display.IMultiLayerLineSymbol)

        from renderer.feature.lines.lineSymbol import LineSymbol
        if multilayer_symbol:
            symbol_collection = SymbolPropertiesProvider.get_multilayer_symbol_collection(multilayer_symbol)

            for symbol in symbol_collection:
                print symbol
                symbol_properties['layer'].append(LineSymbol.create_feature_line_symbol(symbol))
        else:
            symbol_properties['layer'].append(LineSymbol.create_feature_line_symbol(i_symbol))

    @staticmethod
    def get_point_properties(symbol_properties, i_symbol):
        """ This function collects all properties of the point symbol

        :param symbol_properties: This is a dictionary for the properties of a symbol
        :param i_symbol: this is the used polygon symbol
        """
        symbol_properties['symbol_type'] = "marker"
        symbol_properties['layer'] = []
        multilayer_symbol = type_cast_arc_object(i_symbol, ArcGisModules.module_display.IMultiLayerMarkerSymbol)

        if multilayer_symbol:
            symbol_collection = SymbolPropertiesProvider.get_multilayer_symbol_collection(multilayer_symbol)

            for symbol in symbol_collection:
                symbol_properties['layer'].append(
                    SimpleMarkerSymbol.create_simple_marker_symbol(symbol))
        else:
            symbol_properties['layer'].append(
                SimpleMarkerSymbol.create_simple_marker_symbol(i_symbol))

    @staticmethod
    def get_multilayer_symbol_collection(multilayer_symbol):
        """ This returns a list of all the different symbols in a multilayer symbol

        :param multilayer_symbol: the multilayer symbol you want to read out
        :return: the symbol_collection, a list of the symbols from the multilayer symbol
        """
        symbol_collection = []
        for x in range(0, multilayer_symbol.LayerCount):
            symbol_collection.append(multilayer_symbol.Layer[x])
        return symbol_collection

