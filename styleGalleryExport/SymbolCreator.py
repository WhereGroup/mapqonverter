import arcpy

from StyleGalleryItemProvider import StyleGalleryItemProvider
from modules.arcGisModules import ArcGisModules
from renderer.feature.symbols.simpleSymbol import SimpleSymbol
from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider
from modules.functions import change_interface


class SymbolCreator:
    def __init__(self, xml_document):
        self.xml_document = xml_document

    def create_symbols(self, style_gallery, style_gallery_name, class_to_export):
        """ This creates the symbols out of a style-gallery

        :param style_gallery: the main style gallery
        :param style_gallery_name: the gallery to read from
        :param class_to_export: The name of the class to export
        """

        try:
            symbols_element = self.xml_document.getElementsByTagName("symbols")[0]
        except IndexError:
            symbols_element = self.xml_document.createElement("symbols")
        root_element = self.xml_document.getElementsByTagName("qgis_style")[0]
        root_element.appendChild(symbols_element)

        style_gallery_items = StyleGalleryItemProvider.get_style_gallery_items(style_gallery,
                                                                               class_to_export,
                                                                               style_gallery_name
                                                                               )
        if len(style_gallery_items) > 0:
            arcpy.AddMessage("Export {}".format(class_to_export))
        for item in style_gallery_items:
            try:
                i_symbol = change_interface(item.Item, ArcGisModules.module_display.ISymbol)

                symbol_properties = {}
                SymbolPropertiesProvider.get_symbol_properties_by_symbol_class(
                    symbol_properties,
                    i_symbol,
                    class_to_export
                )
                tags = change_interface(item, ArcGisModules.module_display.IStyleGalleryItem2)\
                    .Tags\
                    .replace(";", " ,")

                SimpleSymbol.create_simple_symbol(self.xml_document,
                                                  symbols_element,
                                                  symbol_properties,
                                                  item.Name,
                                                  "1",
                                                  tags
                                                  )
            except (ValueError, Exception):
                arcpy.AddMessage("Error while Exporting {}".format(item.name))
                continue
