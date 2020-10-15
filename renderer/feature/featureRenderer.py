import arcpy
from comtypes import COMError
from modules.functions import change_interface
from modules.arcGisModules import ArcGisModules
from renderer.feature.graduatedColorsRenderer import GraduatedColorsRenderer
from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider
from renderer.feature.uniqueValueRenderer import UniqueValueRenderer
from renderer.feature.symbols.simpleSymbol import SimpleSymbol


class FeatureRenderer:
    
    def __init__(self):
        pass

    @staticmethod
    def create_feature_renderer(base):
        """This creates the feature-renderer-element in the DOM

        :param base: is the self of the renderer object containing:
            base.xml_document = xml_document
            base.map_layer_element = map_layer_element
            base.arcLayer = arc_layer
            base.layer = layer
            base.rendererType = renderer_type
        """
        renderer = base.xml_document.createElement("renderer-v2")
        renderer.setAttribute("forceraster", "0")
        renderer.setAttribute("enableorderby", "0")
        renderer.setAttribute("symbollevels", "0")
        base.map_layer_element.appendChild(renderer)

        symbols_element = base.xml_document.createElement("symbols")
        renderer.appendChild(symbols_element)

        symbols = []

        arc_feature_layer = change_interface(base.arcLayer, ArcGisModules.module_carto.IFeatureLayer)
        arc_geo_feature_layer = change_interface(arc_feature_layer, ArcGisModules.module_carto.IGeoFeatureLayer)
        simple_renderer = arc_geo_feature_layer.Renderer

        # get a feature, mostly 0 , but can be higher, if using objects from a db -> than takes the id
        feature = None
        try:
            for i in range(0, 1000):
                try:
                    feature = arc_feature_layer.FeatureClass.GetFeature(i)
                    break
                except COMError:
                    i += 1
        except AttributeError:
            arcpy.AddWarning("\t\tFinding a Feature to render failed.")
            print "Something went wrong. Are you using a DB where the IDs start at 1001?"
            pass

        if base.layer.symbologyType == "OTHER":
            renderer.setAttribute("type", "singleSymbol")
            symbols.append(simple_renderer.SymbolByFeature(feature))

        elif base.layer.symbologyType == "UNIQUE_VALUES":
            UniqueValueRenderer.create_unique_values_element(base, renderer, symbols)

        elif base.layer.symbologyType == "GRADUATED_COLORS" or "GRADUATED_SYMBOLS":
            GraduatedColorsRenderer.create_graduated_colors_element(base, renderer, symbols)

        try:
            arc_feature_layer = change_interface(base.arcLayer, ArcGisModules.module_carto.IFeatureLayer)
            layer_effects = change_interface(arc_feature_layer, ArcGisModules.module_carto.ILayerEffects)
            alpha = str(1 - layer_effects.Transparency * 0.01)
        except AttributeError:
            alpha = "1"

        # create the symbol element, one for single symbol, more for graduated or unique values
        for count, iSymbol in enumerate(symbols):
            symbol_properties = {}
            if arc_geo_feature_layer.DisplayFeatureClass.ShapeType == 4:
                SymbolPropertiesProvider.get_polygon_properties(symbol_properties, iSymbol)

            elif arc_geo_feature_layer.DisplayFeatureClass.ShapeType == 3:
                SymbolPropertiesProvider.get_line_properties(symbol_properties, iSymbol)

            elif (arc_geo_feature_layer.DisplayFeatureClass.ShapeType == 2) | \
                    (arc_geo_feature_layer.DisplayFeatureClass.ShapeType == 1):
                SymbolPropertiesProvider.get_point_properties(symbol_properties, iSymbol)

            SimpleSymbol.create_simple_symbol(base.xml_document, symbols_element, symbol_properties, count, alpha)

