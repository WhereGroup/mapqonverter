import logging

from BackgroundPageElement import BackGroundPageElement
from geometryElement import GeometryElement
from unit_provider import UnitProvider
from polygonElement import PolygonElement
from lineElement import LineElement
from pictureElement import PictureElement
from zValueProvider import ZValueProvider
from layoutUuidProvider import LayoutUuidProvider
from northArrowElement import NorthArrowElement
from scaleBarElement import ScaleBarElement
from legendElement import LegendElement
from layoutItemFrame import LayoutItemFrame
from layoutItemPropertiesProvider import LayoutItemPropertiesProvider
from layoutItemText import LayoutItemText
from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface
from dictionaries.layoutItemsDict import dict_units


class Layout:
    def __init__(self, dom, qgis, arc_doc, mxd):
        """

        :param dom: the Document Object Model
        :param qgis: the main element of the dom
        :param arc_doc: the ArcObject IMxDocument
        :param mxd: the arcpy mxd-document
        """
        self.dom = dom
        self.qgis = qgis
        self.arc_doc = arc_doc
        self.mxd = mxd

    def create_layout(self):
        """ This is the Main-Function to create the Layout
        It collects all layout-items and creates the content for each one.
        """
        units = self.arc_doc.PageLayout.Page.Units
        UnitProvider.set_origin_unit(units)
        self.arc_doc.PageLayout.Page.Units = 7

        layout_element_dom = Layout.create_base_layout_element(self)
        layout_item_list = Layout.get_layout_items(self)

        for item in layout_item_list:
            try:
                item_type = LayoutItemPropertiesProvider.get_layout_item_type(item)
                Layout.create_item_content(self, item_type, item, layout_element_dom)
            except (KeyError, Exception) as error:
                item_properties = change_interface(item, ArcGisModules.module_carto.IElementProperties3)
                logging.error(u"Error while exporting {} - type: {}".format(
                    item_properties.Name,
                    item_properties.Type
                ))
                logging.error(error.message)
                logging.exception(error)
                continue

        self.arc_doc.PageLayout.Page.Units = UnitProvider.get_origin_unit()

    def create_base_layout_element(self):
        """
        This the creation for the layout, background, etc what is necessary for the layout in general not item-specific
        """

        layout_units = dict_units[self.arc_doc.PageLayout.Page.Units]

        layouts_main_element = self.dom.createElement("Layouts")
        self.qgis.appendChild(layouts_main_element)

        layout_element_dom = self.dom.createElement("Layout")
        layout_element_dom.setAttribute("name", "imported_layout")
        layout_element_dom.setAttribute("units", layout_units)
        layout_element_dom.setAttribute("printResolution", "300")
        LayoutUuidProvider.create_uuid(self.arc_doc.FocusMap.Name)
        layout_element_dom.setAttribute("worldFileMap", LayoutUuidProvider.uuid_dict[self.arc_doc.FocusMap.Name])
        layouts_main_element.appendChild(layout_element_dom)

        snapper_element = self.dom.createElement("Snapper")
        snapper_element.setAttribute("tolerance", "5")
        snapper_element.setAttribute("snapToGrid", "0")
        snapper_element.setAttribute("snapToItems", "1")
        snapper_element.setAttribute("snapToGuides", "1")
        layout_element_dom.appendChild(snapper_element)

        grid_element = self.dom.createElement("Grid")
        grid_element.setAttribute("offsetX", "0")
        grid_element.setAttribute("resolution", "10")
        grid_element.setAttribute("resUnits", "mm")
        grid_element.setAttribute("offsetY", "0")
        grid_element.setAttribute("offsetUnits", "mm")
        layout_element_dom.appendChild(grid_element)

        page_collection_element = self.dom.createElement("PageCollection")
        BackGroundPageElement(self.dom, page_collection_element, self.mxd, self.arc_doc).create_background_layout_item()
        layout_element_dom.appendChild(page_collection_element)

        return layout_element_dom

    def create_item_content(self, layout_item_type, layout_item, layout_element_dom):
        """
        The Item specific layout creation is done here.
        :param layout_item_type: The tyoe of the layout-item
        :param layout_item: the item itself
        :param layout_element_dom: the main layout_element in the dom
        """
        if layout_item_type == 'Text':
            layout_text_item = change_interface(layout_item, ArcGisModules.module_carto.ITextElement)
            text_item = LayoutItemText(self.dom, layout_element_dom, layout_text_item, self.mxd, self.arc_doc)
            text_basic_layout = text_item.create_layout_item_basic()
            text_item.create_text_content(text_basic_layout)

        elif layout_item_type == 'Data Frame':
            layout_map_item = change_interface(layout_item, ArcGisModules.module_carto.IMapFrame)
            if layout_map_item:
                map_item = LayoutItemFrame(self.dom, layout_element_dom, layout_map_item, self.mxd, self.arc_doc)
                map_basic_layout = map_item.create_layout_item_basic()
                map_item.create_map_content(map_basic_layout)

        elif layout_item_type == 'Legend':
            map_surround_frame = change_interface(layout_item, ArcGisModules.module_carto.IMapSurroundFrame)
            legend_item = LegendElement(self.dom, layout_element_dom, map_surround_frame, self.mxd, self.arc_doc)
            legend_basic_layout = legend_item.create_layout_item_basic()
            legend_item.create_legend_content(legend_basic_layout)

        elif layout_item_type == 'North Arrow':
            map_surround_frame = change_interface(layout_item, ArcGisModules.module_carto.IMapSurroundFrame)
            north_arrow_item = NorthArrowElement(self.dom, layout_element_dom, map_surround_frame, self.mxd, self.arc_doc)
            north_arrow_basic_layout = north_arrow_item.create_layout_item_basic()
            north_arrow_item.create_north_arrow_content(north_arrow_basic_layout)

        elif layout_item_type == 'Scale Bar':
            map_surround_frame = change_interface(layout_item, ArcGisModules.module_carto.IMapSurroundFrame)
            scale_bar_item = ScaleBarElement(self.dom, layout_element_dom, map_surround_frame, self.mxd, self.arc_doc)
            scale_bar_basic_layout = scale_bar_item.create_layout_item_basic()
            scale_bar_item.create_scale_bar_content(scale_bar_basic_layout)

        elif layout_item_type in ['Rectangle', 'Ellipse', 'Circle', 'Rechteck', 'Kreis']:
            fill_symbol_element = change_interface(layout_item, ArcGisModules.module_carto.IFillShapeElement)
            geometry_element = GeometryElement(self.dom, layout_element_dom, fill_symbol_element, self.mxd, self.arc_doc)
            geometry_element_layout = geometry_element.create_layout_item_basic()
            geometry_element.create_geometry_element_content(geometry_element_layout, layout_item_type)

        elif layout_item_type == 'Line' or 'Linie':
            line_symbol = change_interface(layout_item, ArcGisModules.module_carto.ILineElement)
            line_element = LineElement(self.dom, layout_element_dom, line_symbol, self.mxd, self.arc_doc)
            line_element_layout = line_element.create_layout_item_basic()
            line_element.create_line_element_content(line_element_layout)

        elif layout_item_type == 'Polygon':
            fill_symbol_element = change_interface(layout_item, ArcGisModules.module_carto.IFillShapeElement)
            polygon_element = PolygonElement(self.dom, layout_element_dom, fill_symbol_element, self.mxd, self.arc_doc)
            polygon_element_layout = polygon_element.create_layout_item_basic()
            polygon_element.create_geometry_element_content(polygon_element_layout)

        elif layout_item_type == 'Picture' or 'Bild':
            picture_element_arc = change_interface(layout_item, ArcGisModules.module_carto.IPictureElement3)
            picture_element = PictureElement(self.dom, layout_element_dom, picture_element_arc, self.mxd, self.arc_doc)
            picture_element_layout = picture_element.create_layout_item_basic()
            picture_element.create_picture_content(picture_element_layout)

        else:
            logging.info(u"{} is not yet supported".format(layout_item_type))

    def get_layout_items(self):
        """
        This function collects all layout-items and returns them as a list
            additionally it tells the ZValueProvider the number of items +1 (because of the background element)
        :return: a list of the layout-items
        """

        if self.arc_doc.ActiveView.IsMapActivated:
            self.arc_doc.ActiveView = self.arc_doc.PageLayout

        graphics_container_select = change_interface(self.arc_doc.PageLayout,
                                                     ArcGisModules.module_carto.IGraphicsContainerSelect)
        graphics_container_select.SelectAllElements()
        all_layout_elements = graphics_container_select.SelectedElements
        count = graphics_container_select.ElementSelectionCount

        layout_element_object_list = []
        for times in range(count):
            layout_element_object_list.append(all_layout_elements.next())

        ZValueProvider.number_of_elements = len(layout_element_object_list) + 1
        graphics_container_select.UnselectAllElements()

        return layout_element_object_list



