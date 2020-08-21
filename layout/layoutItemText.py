from layoutItem import LayoutItem
from modules.functions import convert_int_to_rgb_string
from dictionaries.textSymbol import TextSymbol


class LayoutItemText(LayoutItem):

    def __init__(self, dom, parent_element, text_object, mxd, arc_doc):
        """
        This function creates a Text-Item for the layout
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param text_object: The text-object itself as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, text_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.text_object = text_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_text_content(self, layout_item_base_element):
        """
        This function creats the Text-item specific content
        :param layout_item_base_element: the layout element in the DOM
        """
        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.layout_item_object)
        LayoutItemText.set_size_and_position(self, layout_item_base_element, arcpy_item)

        font_symbol = self.text_object.Symbol

        layout_item_base_element.setAttribute("frame", "false")
        layout_item_base_element.setAttribute("background", "false")
        layout_item_base_element.setAttribute("type", "65641")
        layout_item_base_element.setAttribute("labelText", font_symbol.Text)
        layout_item_base_element.setAttribute("marginX", "0")
        layout_item_base_element.setAttribute("marginY", "0")
        layout_item_base_element.setAttribute("halign",
                                              TextSymbol.textSymbolHorizontalAlign[
                                                  font_symbol.HorizontalAlignment
                                              ])
        layout_item_base_element.setAttribute("valign",
                                              TextSymbol.textSymbolVerticalAlign[
                                                  font_symbol.VerticalAlignment
                                              ])

        LayoutItemText.set_uuid_attributes(arcpy_item.text[:5], layout_item_base_element)
        label_font_description = LayoutItemText.get_label_font_description(font_symbol)

        label_font_element = self.dom.createElement("LabelFont")
        label_font_element.setAttribute("description", label_font_description)
        layout_item_base_element.appendChild(label_font_element)

        font_color = convert_int_to_rgb_string(font_symbol.Color.RGB).split(",")
        font_color_element = self.dom.createElement("FontColor")
        font_color_element.setAttribute('red', font_color[0])
        font_color_element.setAttribute('green', font_color[1])
        font_color_element.setAttribute('blue', font_color[2])
        font_color_element.setAttribute('alpha', font_color[3])
        layout_item_base_element.appendChild(font_color_element)
