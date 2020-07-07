from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_arc_object
from renderer.feature.symbols.simpleSymbol import SimpleSymbol
from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider
from layoutItem import LayoutItem


class PolygonElement(LayoutItem):
    def __init__(self, dom, parent_element, polygon_object, mxd, arc_doc):
        """
        This function creates a Polygon-Item for the layout
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param polygon_object: the polygon_object as ArcObject 
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, polygon_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.polygon_object = polygon_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_geometry_element_content(self, polygon_element_layout):
        """
        This function creats the polygon-item specific content
        :param polygon_element_layout: the layout element in the DOM
        """
        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.polygon_object)
        PolygonElement.set_size_and_position(self, polygon_element_layout, arcpy_item)

        polygon_element_layout.setAttribute('type', '65644')
        polygon_element_layout.setAttribute("frame", "false")
        polygon_element_layout.setAttribute("background", "false")

        PolygonElement.set_uuid_attributes(arcpy_item.name, polygon_element_layout)

        symbol = type_cast_arc_object(self.polygon_object, ArcGisModules.module_carto.IFillShapeElement).Symbol
        symbol_properties = {}

        SymbolPropertiesProvider.get_polygon_properties(symbol_properties, symbol)

        SimpleSymbol.create_simple_symbol(self.dom, polygon_element_layout, symbol_properties, 1, '1')

        element_geometry = type_cast_arc_object(self.polygon_object, ArcGisModules.module_carto.IElement).Geometry
        polygon_symbol = type_cast_arc_object(element_geometry, ArcGisModules.module_geometry.IPolygon5)
        point_collection = type_cast_arc_object(polygon_symbol, ArcGisModules.module_geometry.IPointCollection)

        PolygonElement.create_nodes(self, polygon_element_layout, point_collection, arcpy_item)
