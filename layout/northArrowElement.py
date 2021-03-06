from layoutItem import LayoutItem
from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface, convert_int_to_rgb_string


class NorthArrowElement(LayoutItem):

    def __init__(self, dom, parent_element, north_arrow_object, mxd, arc_doc):
        """
        This function creates a NorthArrow-item
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param north_arrow_object: the northArrow as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, north_arrow_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.north_arrow_object = north_arrow_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_north_arrow_content(self, layout_item_base_element):
        """
        This function creats the northArrow-item specific content
        :param layout_item_base_element: the layout element in the DOM
        """
        border = self.north_arrow_object.Border
        background = self.north_arrow_object.Background

        NorthArrowElement.create_background_and_frame(self, border, background, layout_item_base_element)

        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.layout_item_object)
        NorthArrowElement.set_size_and_position(self, layout_item_base_element, arcpy_item)

        NorthArrowElement.set_uuid_attributes(self.layout_item_object.MapSurround.Name, layout_item_base_element)

        layout_item_base_element.setAttribute('file', ":/images/north_arrows/layout_default_north_arrow.svg")
        layout_item_base_element.setAttribute('type', "65640")
        north_arrow = change_interface(self.north_arrow_object.MapSurround, ArcGisModules.module_carto.INorthArrow)
        layout_item_base_element.setAttribute('northOffset', unicode(north_arrow.CalibrationAngle))
        layout_item_base_element.setAttribute('svgBorderColor', convert_int_to_rgb_string(north_arrow.Color.RGB))
        layout_item_base_element.setAttribute('svgFillColor', "255,255,255,255")

