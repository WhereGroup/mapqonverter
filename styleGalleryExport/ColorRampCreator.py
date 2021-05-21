import arcpy

from StyleGalleryItemProvider import StyleGalleryItemProvider
from modules.arcGisModules import ArcGisModules
from renderer.feature.fills.gradientFillSymbol import FeatureGradientFillSymbol
from modules.functions import change_interface


class ColorRampCreator:
    def __init__(self, xml_document):
        self.xml_document = xml_document

    def create_colorramps(self, style_gallery, style_gallery_name):
        """ This creates the colorramps out of a style-gallery

        :param style_gallery: the main style gallery
        :param style_gallery_name: the gallery to read from
        """
        color_ramps_element = self.xml_document.createElement("colorramps")
        root_element = self.xml_document.getElementsByTagName("qgis_style")[0]
        root_element.appendChild(color_ramps_element)

        style_gallery_items = StyleGalleryItemProvider.get_style_gallery_items(style_gallery,
                                                                               "Color Ramps",
                                                                               style_gallery_name
                                                                               )
        if len(style_gallery_items) > 0:
            arcpy.AddMessage("Export {}".format("Color Ramps"))

        for item in style_gallery_items:
            try:
                color_ramp = change_interface(item.Item, ArcGisModules.module_display.IColorRamp)

                symbol_properties = {
                    'ramp_name': item.Name,
                    'tag': style_gallery_name.split(".")[0],
                    'dict_symbols': {},
                }

                FeatureGradientFillSymbol.create_color_ramp_properties(color_ramp, False, symbol_properties)

                ColorRampCreator.write_colorramp_in_xml(self, symbol_properties)

            except (ValueError, Exception):
                arcpy.AddMessage("Error while Exporting {}".format(item.name))
                continue

    def write_colorramp_in_xml(self, symbol_properties):
        """ This creates the colorramp element in the DOM

        :param symbol_properties: the properties of the colorramp
        """
        color_ramp_element = self.xml_document.createElement("colorramp")
        color_ramp_element.setAttribute("type", "gradient")
        color_ramp_element.setAttribute("name", symbol_properties["ramp_name"])
        color_ramp_element.setAttribute("tags", symbol_properties["tag"])

        for key, value in symbol_properties["dict_symbols"].iteritems():
            property_element = self.xml_document.createElement("prop")
            property_element.setAttribute("k", key)
            property_element.setAttribute("v", value)
            color_ramp_element.appendChild(property_element)

        ramp_type_property_element = self.xml_document.createElement('prop')
        ramp_type_property_element.setAttribute("rampType", "gradient")
        color_ramp_element.appendChild(ramp_type_property_element)

        parent_element = self.xml_document.getElementsByTagName("colorramps")[0]
        parent_element.appendChild(color_ramp_element)
