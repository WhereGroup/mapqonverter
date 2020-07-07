from renderer.feature.symbols.simpleSymbol import SimpleSymbol
from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider
from layoutItem import LayoutItem
from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_arc_object


class LineElement(LayoutItem):
    def __init__(self, dom, parent_element, line_object, mxd, arc_doc):
        """
        This function creates a Line-Item for the layout
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param line_object: the line_object as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, line_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.line_object = line_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_line_element_content(self, line_element_layout):
        """
        This function creats the Line-item specific content
        :param line_element_layout: the layout element in the DOM
        """
        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.line_object)
        LineElement.set_size_and_position(self, line_element_layout, arcpy_item)

        element_geometry = type_cast_arc_object(self.line_object, ArcGisModules.module_carto.IElement).Geometry
        poly_ine_symbol = type_cast_arc_object(element_geometry, ArcGisModules.module_geometry.IPolyline5)
        point_collection = type_cast_arc_object(poly_ine_symbol, ArcGisModules.module_geometry.IPointCollection)

        line_element_layout.setAttribute('type', '65645')
        line_element_layout.setAttribute("frame", "false")
        line_element_layout.setAttribute("background", "false")

        LineElement.set_uuid_attributes(arcpy_item.name, line_element_layout)

        symbol = self.line_object.Symbol
        symbol_properties = {}

        SymbolPropertiesProvider.get_line_properties(symbol_properties, symbol)

        SimpleSymbol.create_simple_symbol(self.dom, line_element_layout, symbol_properties, 1, '1')

        LineElement.create_nodes(self, line_element_layout, point_collection, arcpy_item)

