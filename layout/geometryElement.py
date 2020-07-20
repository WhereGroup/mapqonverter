from dictionaries.layoutItemsDict import dict_geometry
from layoutItem import LayoutItem
from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface
from renderer.feature.symbols.simpleSymbol import SimpleSymbol
from renderer.feature.symbols.symbolPropertiesProvider import SymbolPropertiesProvider


class GeometryElement(LayoutItem):

    def __init__(self, dom, parent_element, geometry_object, mxd, arc_doc):
        """
        This function creates a geometry layout-item
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param geometry_object: the geometry-object itself as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, geometry_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.geometry_object = geometry_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_geometry_element_content(self, geometry_element_layout, geometry_type):
        """
        This function creates the geometry specific content
        :param geometry_element_layout: the geometry layout element in the DOM
        :param geometry_type: the shape type as string
        """
        
        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.layout_item_object)

        GeometryElement.set_size_and_position(self, geometry_element_layout, arcpy_item)

        geometry_element_layout.setAttribute("frame", "false")
        geometry_element_layout.setAttribute("background", "false")

        geometry_element_layout.setAttribute('shapeType', dict_geometry[geometry_type])
        geometry_element_layout.setAttribute('type', "65643")

        GeometryElement.set_uuid_attributes(arcpy_item.name, geometry_element_layout)

        symbol = change_interface(self.geometry_object, ArcGisModules.module_carto.IFillShapeElement).Symbol
        symbol_properties = {}

        SymbolPropertiesProvider.get_polygon_properties(symbol_properties, symbol)

        SimpleSymbol.create_simple_symbol(self.dom, geometry_element_layout, symbol_properties, 1, '1')

