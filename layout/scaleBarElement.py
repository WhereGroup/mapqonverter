from dictionaries.layoutItemsDict import dict_units, dict_vertical_position, dict_line_style
from layoutUuidProvider import LayoutUuidProvider
from layoutItem import LayoutItem
from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_module, unpack2rgb


class ScaleBarElement(LayoutItem):

    def __init__(self, dom, parent_element, scale_bar_object, mxd, arc_doc):
        """
        This function creates a ScaleBar-Item for the layout
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param scale_bar_object: The ScaleBarObject as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, scale_bar_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.scale_bar_object = scale_bar_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_scale_bar_content(self, layout_item_base_element):
        """
        This function creats the ScaleBar-item specific content
        :param layout_item_base_element: the layout element in the DOM
        """

        border = self.scale_bar_object.Border
        background = self.scale_bar_object.Background

        ScaleBarElement.create_background_and_frame(self, border, background, layout_item_base_element)

        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.layout_item_object)
        ScaleBarElement.set_size_and_position(self, layout_item_base_element, arcpy_item)

        scale_bar = type_cast_module(self.scale_bar_object.MapSurround, ArcGisModules.module_carto.IScaleBar)
        scale_marks = type_cast_module(self.scale_bar_object.MapSurround, ArcGisModules.module_carto.IScaleMarks)

        layout_item_base_element.setAttribute('unitType', dict_units[scale_bar.Units])
        layout_item_base_element.setAttribute('unitLabel', scale_bar.UnitLabel)

        ScaleBarElement.set_uuid_attributes(self.layout_item_object.MapSurround.Name, layout_item_base_element)

        try:
            layout_item_base_element.setAttribute(
                'mapUuid', 
                unicode(LayoutUuidProvider.uuid_dict[self.layout_item_object.MapSurround.Map.Name])
            )
        except KeyError:
            LayoutUuidProvider.create_uuid(self.layout_item_object.MapSurround.Map.Name)
            layout_item_base_element.setAttribute('mapUuid', unicode(
                LayoutUuidProvider.uuid_dict[self.layout_item_object.MapSurround.Map.Name])
                                                  )

        layout_item_base_element.setAttribute('type', "65646")
        layout_item_base_element.setAttribute('numSegments', unicode(scale_bar.Divisions-scale_bar.DivisionsBeforeZero))
        if scale_bar.DivisionsBeforeZero > 0:
            layout_item_base_element.setAttribute('numSegmentsLeft', unicode(scale_bar.Subdivisions))
        else:
            layout_item_base_element.setAttribute('numSegmentsLeft', '0')
        layout_item_base_element.setAttribute('numUnitsPerSegment', unicode(scale_bar.Division))
        layout_item_base_element.setAttribute('labelVerticalPlacement', dict_vertical_position[scale_bar.LabelPosition])
        layout_item_base_element.setAttribute('labelBarSpace', unicode(scale_bar.LabelGap))
        if str(scale_bar.Name).startswith('Double'):
            layout_item_base_element.setAttribute('style', "Double Box")
        else:
            layout_item_base_element.setAttribute('style', "Single Box")

        scale_line = type_cast_module(scale_bar, ArcGisModules.module_carto.IScaleLine)
        if scale_line:
            layout_item_base_element.setAttribute('numSegments',
                                                  unicode(
                                                      (scale_bar.Divisions - scale_bar.DivisionsBeforeZero) * 
                                                      scale_bar.Subdivisions
                                                  )
                                                  )
            layout_item_base_element.setAttribute('numUnitsPerSegment', unicode(
                scale_bar.Division / scale_bar.Subdivisions)
                                                  )
            layout_item_base_element.setAttribute('style', dict_line_style[scale_marks.MarkPosition])

        double_fill_scale_bar = type_cast_module(scale_bar, ArcGisModules.module_carto.IDoubleFillScaleBar)

        if double_fill_scale_bar:
            fill_color_1 = unpack2rgb(double_fill_scale_bar.FillSymbol1.Color.RGB).split(",")
            fill_color_2 = unpack2rgb(double_fill_scale_bar.FillSymbol2.Color.RGB).split(",")
        else:
            fill_color_1 = unpack2rgb(scale_bar.BarColor.RGB).split(',')
            fill_color_2 = "255,255,255,255"

        fill_color_1_element = self.dom.createElement('fillColor')
        fill_color_1_element.setAttribute('red', fill_color_1[0])
        fill_color_1_element.setAttribute('green', fill_color_1[1])
        fill_color_1_element.setAttribute('blue', fill_color_1[2])
        fill_color_1_element.setAttribute('alpha', fill_color_1[3])
        layout_item_base_element.appendChild(fill_color_1_element)

        fill_color_2_element = self.dom.createElement('fillColor2')
        fill_color_2_element.setAttribute('red', fill_color_2[0])
        fill_color_2_element.setAttribute('green', fill_color_2[1])
        fill_color_2_element.setAttribute('blue', fill_color_2[2])
        fill_color_2_element.setAttribute('alpha', fill_color_2[3])
        layout_item_base_element.appendChild(fill_color_2_element)
