import copy
import arcpy

from StyleGalleryItemProvider import StyleGalleryItemProvider
from modules.arcGisModules import ArcGisModules
from dictionaries.label_dict import labelDict
from modules.functions import change_interface
from renderer.labelRenderer import LabelRenderer


class TextFormatCreator:
    def __init__(self, xml_document):
        self.xml_document = xml_document

    def create_text_formats(self, style_gallery, style_gallery_name):
        """ This creates the text symbols out of a style-gallery

        :param style_gallery: the main style gallery
        :param style_gallery_name: the gallery to read from
        """
        textformats_element = self.xml_document.createElement("textformats")
        root_element = self.xml_document.getElementsByTagName("qgis_style")[0]
        root_element.appendChild(textformats_element)

        style_gallery_items = StyleGalleryItemProvider.get_style_gallery_items(style_gallery,
                                                                               "Text Symbols",
                                                                               style_gallery_name
                                                                               )
        if len(style_gallery_items) > 0:
            arcpy.AddMessage("Export {}".format("Text Symbols"))

        for item in style_gallery_items:
            try:
                textformat_element = self.xml_document.createElement("textformat")
                textformat_element.setAttribute("name", item.Name)
                tags = change_interface(item, ArcGisModules.module_display.IStyleGalleryItem2) \
                    .Tags \
                    .replace(";", " ,")
                textformat_element.setAttribute("tags", tags)
                textformats_element.appendChild(textformat_element)

                formatted_symbol = change_interface(item.Item, ArcGisModules.module_display.IFormattedTextSymbol)

                label_dict = copy.deepcopy(labelDict)

                LabelRenderer.get_text_style(formatted_symbol, label_dict)
                LabelRenderer.get_background(formatted_symbol, label_dict)

                LabelRenderer.create_text_style_element(textformat_element, self.xml_document, label_dict)

            except (ValueError, Exception):
                arcpy.AddMessage("Error while Exporting {}".format(item.name))
                continue
