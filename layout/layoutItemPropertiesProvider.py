from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_module


class LayoutItemPropertiesProvider:
    def __init__(self):
        pass

    @staticmethod
    def get_item_properties(item):
        """
        This function returns the properties of an LayoutElement
        :param item: the item as ArcObject
        :return: the properties of an item as ArcObject
        """
        element = type_cast_module(item, ArcGisModules.module_carto.IElement)
        properties = type_cast_module(element, ArcGisModules.module_carto.IElementProperties3)

        return properties

    @staticmethod
    def get_layout_item_type(layout_item, properties=None):
        """
        This function returns the item-type from an arcObject
        :param layout_item: the item as ArcObject
        :param properties: if properties have been collected they can be declared
        :return: the type of the item as string
        """
        if properties is None:
            properties = LayoutItemPropertiesProvider.get_item_properties(layout_item)
        layout_item_type = properties.Type
        if layout_item_type == u'Map Surround Frame':
            map_surround_frame = type_cast_module(layout_item, ArcGisModules.module_carto.IMapSurroundFrame)
            legend = type_cast_module(map_surround_frame.MapSurround, ArcGisModules.module_carto.ILegend2)
            north_arrow = type_cast_module(map_surround_frame.MapSurround, ArcGisModules.module_carto.INorthArrow)
            scale_bar = type_cast_module(map_surround_frame.MapSurround, ArcGisModules.module_carto.IScaleBar)
            if legend:
                layout_item_type = u'Legend'
            if north_arrow:
                layout_item_type = u'North Arrow'
            if scale_bar:
                layout_item_type = u'Scale Bar'
        return layout_item_type
