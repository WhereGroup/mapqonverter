import arcpy

from dictionaries.layoutItemsDict import dict_arcpy_arcObj_types, dict_units
from unit_provider import UnitProvider
from layoutUuidProvider import LayoutUuidProvider
from zValueProvider import ZValueProvider
from layoutItemPropertiesProvider import LayoutItemPropertiesProvider
from modules.arcGisModules import ArcGisModules
from modules.functions import convert_int_to_rgb_string, change_interface, is_close


class LayoutItem:
    def __init__(self, dom, parent_element, layout_item_object, mxd, arc_doc):
        """
        This function creates a layout-item
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param layout_item_object: the layout-item itself as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        self.dom = dom
        self.parent_element = parent_element
        self.layout_item_object = layout_item_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_layout_item_basic(self):
        """
        This creates the basic properties for a layout item.
        :return: return the item-layout as a dom object.
        """

        item_properties = LayoutItemPropertiesProvider.get_item_properties(self.layout_item_object)
        anchor_point = "0"
        if item_properties:
            anchor_point = unicode(item_properties.AnchorPoint)

        layout_item_element = self.dom.createElement("LayoutItem")
        layout_item_element.setAttribute("frame", "true")
        layout_item_element.setAttribute("background", "true")
        layout_item_element.setAttribute("referencePoint", anchor_point)

        layout_item_element.setAttribute("visibility", "1")
        layout_item_element.setAttribute("excludeFromExports", "0")
        layout_item_element.setAttribute("id", "")
        layout_item_element.setAttribute("opacity", "1")
        layout_item_element.setAttribute("blendMode", "0")
        layout_item_element.setAttribute("itemRotation", "0")
        layout_item_element.setAttribute('zValue', ZValueProvider.get_z_value())

        self.parent_element.appendChild(layout_item_element)

        layout_object_element = self.dom.createElement("LayoutObject")
        layout_item_element.appendChild(layout_object_element)

        dd_properties_element = self.dom.createElement("dataDefined_properties")
        layout_object_element.appendChild(dd_properties_element)

        option_element = self.dom.createElement("Option")
        option_element.setAttribute('type', 'Map')
        dd_properties_element.appendChild(option_element)

        option_child1_element = self.dom.createElement("Option")
        option_child1_element.setAttribute('type', 'QString')
        option_child1_element.setAttribute('name', 'name')
        option_child1_element.setAttribute('value', '')
        option_element.appendChild(option_child1_element)

        option_child2_element = self.dom.createElement("Option")
        option_child2_element.setAttribute('name', 'properties')
        option_element.appendChild(option_child2_element)

        option_child3_element = self.dom.createElement("Option")
        option_child3_element.setAttribute('type', 'QString')
        option_child3_element.setAttribute('name', 'type')
        option_child3_element.setAttribute('value', 'collection')
        option_element.appendChild(option_child3_element)

        return layout_item_element

    def create_frame_element(self, layout_item_element, frame_color=0):
        """
        This function creates the frame for a layout-item
        :param layout_item_element: the layout-item as a dom object
        :param frame_color: the color of the frame, default is black
        :return:
        """
        frame_colors = convert_int_to_rgb_string(frame_color).split(",")
        frame_color_element = self.dom.createElement("FrameColor")
        frame_color_element.setAttribute('red', frame_colors[0])
        frame_color_element.setAttribute('green', frame_colors[1])
        frame_color_element.setAttribute('blue', frame_colors[2])
        frame_color_element.setAttribute('alpha', frame_colors[3])
        layout_item_element.appendChild(frame_color_element)

    def create_background_element(self, layout_item_element, background_color=16777215):
        """
        This function creates the background for a layout-item
        :param layout_item_element: the layout-item as a dom object
        :param background_color: the color of the background, default is white
        :return:
        """
        background_colors = convert_int_to_rgb_string(background_color).split(",")
        background_color_element = self.dom.createElement("BackgroundColor")
        background_color_element.setAttribute('red', background_colors[0])
        background_color_element.setAttribute('green', background_colors[1])
        background_color_element.setAttribute('blue', background_colors[2])
        background_color_element.setAttribute('alpha', background_colors[3])
        layout_item_element.appendChild(background_color_element)

    def get_arcpy_layout_element(self, arc_object_item):
        """
        This return the fitting arcpy-item to the arcObject
        :param arc_object_item: the layout-item as arcObject
        :return: the layout-item as arcpy-item
        """
        arcpy_item = None
        properties = LayoutItemPropertiesProvider.get_item_properties(arc_object_item)
        item_type = LayoutItemPropertiesProvider.get_layout_item_type(arc_object_item, properties)
        filter_type = dict_arcpy_arcObj_types[item_type]
        for element in arcpy.mapping.ListLayoutElements(self.mxd, filter_type):
            if self.compare_layout_items(element, arc_object_item, properties, filter_type):
                arcpy_item = element
                break
        return arcpy_item

    @staticmethod
    def compare_layout_items(arcpy_object, arc_object_item, arc_object_item_properties, filter_type):
        """
        This function compares an arcObject item with an arcpy item depending from type-specific properties
        :param arcpy_object: an arcpy item to compare with
        :param arc_object_item: the original arcObject item
        :param arc_object_item_properties: the properties of the arcObject
        :param filter_type: the type of the arcObject
        :return: Boolean if the arcpy item is the same as the compared ArcObject
        """
        result = False
        i_element = change_interface(arc_object_item, ArcGisModules.module_carto.IElement)

        if filter_type == 'TEXT_ELEMENT' \
                and arcpy_object.name == arc_object_item_properties.Name \
                and arcpy_object.text == arc_object_item.Text \
                and LayoutItem.compare_position(arcpy_object, i_element, is_text_element=True):
            result = True
        elif filter_type == 'DATAFRAME_ELEMENT' \
                and arcpy_object.name == arc_object_item_properties.Name \
                and LayoutItem.compare_position(arcpy_object, i_element):
            result = True
        elif filter_type == 'LEGEND_ELEMENT' \
                and arcpy_object.name == arc_object_item_properties.Name \
                and LayoutItem.compare_position(arcpy_object, i_element)\
                and arcpy_object.parentDataFrameName == arc_object_item.MapSurround.Map.Name:
            result = True
        elif filter_type == 'MAPSURROUND_ELEMENT' \
                and arcpy_object.name == arc_object_item_properties.Name \
                and LayoutItem.compare_position(arcpy_object, i_element) \
                and arcpy_object.parentDataFrameName == arc_object_item.MapSurround.Map.Name:
            result = True
        elif filter_type == 'GRAPHIC_ELEMENT' \
                and arcpy_object.name == arc_object_item_properties.Name \
                and LayoutItem.compare_position(arcpy_object, i_element):
            result = True
        elif filter_type == 'PICTURE_ELEMENT' \
                and arcpy_object.name == arc_object_item_properties.Name \
                and LayoutItem.compare_position(arcpy_object, i_element)\
                and arcpy_object.sourceImage[-3:] in arc_object_item.Filter:
            result = True

        return result

    @staticmethod
    def compare_position(arcpy_object, i_element, is_text_element=False):
        """
        Compares the the ArcObject with the Arcpy Layoutitem depending on the layout position
        :param arcpy_object: the arcpy object of the layoutitem
        :param i_element: the arcobject element of the layoutitem
        :param is_text_element: Boolean indicates if element is text-element - default False
        """

        convert_unit_factor = UnitProvider.get_unit_conversion_factor()
        result = False

        # The Arcpy Text-Element has another default anchor-point than the arcObject,
        # because of that the comparison is so weird

        if is_text_element:
            if is_close((arcpy_object.elementPositionY * convert_unit_factor)
                        + (arcpy_object.elementHeight * convert_unit_factor),
                        i_element.Geometry.Envelope.YMin, abs_tol=0.20) \
                and is_close((arcpy_object.elementPositionX * convert_unit_factor)
                             + (arcpy_object.elementWidth * convert_unit_factor / 2),
                             i_element.Geometry.Envelope.XMin, abs_tol=15):
                result = True
        if is_close(arcpy_object.elementPositionY * convert_unit_factor,
                    i_element.Geometry.Envelope.YMin, abs_tol=0.20) \
            and is_close(arcpy_object.elementPositionX * convert_unit_factor,
                         i_element.Geometry.Envelope.XMin, abs_tol=0.20):
            result = True

        return result

    @staticmethod
    def get_label_font_description(font_symbol):
        """
        Based on a font_symbol this function creates a font-description QGIS uses to show a font
        :param font_symbol: the symbol
        :return: a string font-description
        """
        label_font_description = "{font},{size},-1,5,{bold},{italic},{underline},{line_through},0,0".format(
            font=font_symbol.Font.Name,
            size=font_symbol.Size,
            italic=int(font_symbol.Font.Italic),
            bold=75 if font_symbol.Font.Bold else 50,
            underline=int(font_symbol.Font.Underline),
            line_through=int(font_symbol.Font.Strikethrough)
        )

        return label_font_description

    def set_size_and_position(self, layout_item_base_element, arcpy_item):
        """
        This function sets size and position of an layout item
        :param layout_item_base_element: the layout-item in the DOM
        :param arcpy_item: the arcpy item to the layout-item
        """
        target_unit = dict_units[self.arc_doc.PageLayout.Page.Units]

        convert_unit_factor = UnitProvider.get_unit_conversion_factor()

        page_heigth = self.arc_doc.PageLayout.Page.PrintableBounds.Height

        layout_item_base_element.setAttribute("size", "{width},{height},{units}".format(
            height=arcpy_item.elementHeight * convert_unit_factor,
            width=arcpy_item.elementWidth * convert_unit_factor,
            units=target_unit),
                                              )
        layout_item_base_element.setAttribute("position", "{pos_x},{pos_y},{units}".format(
            pos_x=arcpy_item.elementPositionX * convert_unit_factor,
            pos_y=page_heigth - arcpy_item.elementPositionY * convert_unit_factor,
            units=target_unit),
                                              )

    def create_background_and_frame(self, border, background, layout_item_base_element):
        """
        This function creates background and frame properties if these values exist.
        :param border: the border_object as arcObject
        :param background: the background_object as arcObject
        :param layout_item_base_element: the item layout in the DOM
        """
        frame_border_symbol = change_interface(border, ArcGisModules.module_carto.ISymbolBorder)
        frame_background_symbol = change_interface(
            background,
            ArcGisModules.module_carto.ISymbolBackground
        )

        if frame_border_symbol:
            layout_item_base_element.setAttribute("frame", "true")
            LayoutItem.create_frame_element(
                self,
                layout_item_base_element,
                frame_border_symbol.LineSymbol.Color.RGB
            )
            layout_item_base_element.setAttribute(
                "outlineWidthM",
                "{},pt".format(frame_border_symbol.LineSymbol.Width)
            )
        else:
            layout_item_base_element.setAttribute("frame", "false")

        if frame_background_symbol:
            layout_item_base_element.setAttribute("background", "true")
            LayoutItem.create_background_element(
                self,
                layout_item_base_element,
                frame_background_symbol.FillSymbol.Color.RGB
            )
        else:
            layout_item_base_element.setAttribute("background", "false")

    def create_nodes(self, line_element_layout, point_collection, arcpy_item):
        """
        This function creates Nodes for line/polygon -items
        :param line_element_layout: the layout as DOM element
        :param point_collection: the collection of points 
        :param arcpy_item: the arcpy item of the layout item
        """
        nodes_element = self.dom.createElement('nodes')
        line_element_layout.appendChild(nodes_element)
        page_heigth = self.arc_doc.PageLayout.Page.PrintableBounds.Height

        convert_unit_factor = UnitProvider.get_unit_conversion_factor()

        for index in range(0, point_collection.PointCount):
            point = point_collection.Point[index]
            y_coordinate = page_heigth - point.Y - (
                        page_heigth - arcpy_item.elementPositionY * convert_unit_factor
                        - arcpy_item.elementHeight * convert_unit_factor
            )
            node_element = self.dom.createElement('node')
            node_element.setAttribute('x', unicode(point.X - arcpy_item.elementPositionX * convert_unit_factor))
            node_element.setAttribute('y', unicode(y_coordinate))
            nodes_element.appendChild(node_element)

    @staticmethod
    def set_uuid_attributes(element_name, layout_item_base_element):
        """
        Every Item needs a UUID, this function creates this.
        :param element_name: the name of the layout item
        :param layout_item_base_element: the layout in the DOM
        """
        LayoutUuidProvider.create_uuid(element_name)
        uuid = unicode(LayoutUuidProvider.uuid_dict[element_name])
        layout_item_base_element.setAttribute('templateUuid', uuid)
        layout_item_base_element.setAttribute('uuid', uuid)
