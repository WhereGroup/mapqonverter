import copy

import arcpy

from StyleGalleryItemProvider import StyleGalleryItemProvider
from modules.arcGisModules import ArcGisModules
from dictionaries.label_dict import labelDict
from modules.functions import change_interface
from renderer.labelRenderer import LabelRenderer


class LabelSettingsCreator:
    def __init__(self, xml_document):
        self.xml_document = xml_document

    def create_label_settings(self, style_gallery, style_gallery_name):
        """ This creates the labels out of a style-gallery

        :param style_gallery: the main style gallery
        :param style_gallery_name: the gallery to read from
        :return:
        """
        labels_element = self.xml_document.createElement("labelsettings")
        root_element = self.xml_document.getElementsByTagName("qgis_style")[0]
        root_element.appendChild(labels_element)

        style_gallery_items = StyleGalleryItemProvider.get_style_gallery_items(style_gallery,
                                                                               "Labels",
                                                                               style_gallery_name
                                                                               )
        if len(style_gallery_items) > 0:
            arcpy.AddMessage("Export {}".format("Labels"))

        for item in style_gallery_items:
            try:
                label_element = self.xml_document.createElement("labelsetting")
                label_element.setAttribute("name", item.Name)
                tags = change_interface(item, ArcGisModules.module_display.IStyleGalleryItem2) \
                    .Tags \
                    .replace(";", " ,")
                label_element.setAttribute("tags", tags)
                labels_element.appendChild(label_element)

                settings_element = self.xml_document.createElement("settings")
                settings_element.setAttribute("calloutType", "simple")
                label_element.appendChild(settings_element)

                label_style = change_interface(item.Item, ArcGisModules.module_carto.ILabelStyle)
                formatted_symbol = change_interface(label_style.Symbol,
                                                    ArcGisModules.module_display.IFormattedTextSymbol
                                                    )

                label_dict = copy.deepcopy(labelDict)

                LabelRenderer.get_text_style(formatted_symbol, label_dict)
                LabelRenderer.get_background(formatted_symbol, label_dict)

                LabelRenderer.create_text_style_element(settings_element, self.xml_document, label_dict)
                LabelRenderer.create_dd_settings(self.xml_document, settings_element)
                LabelRenderer.create_callout_element(self.xml_document,
                                                     settings_element,
                                                     formatted_symbol.Background
                                                     )
            except (ValueError, Exception):
                arcpy.AddMessage("Error while Exporting {}".format(item.name))
                continue
