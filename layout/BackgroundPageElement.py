from dictionaries.layoutItemsDict import dict_units
from layoutItem import LayoutItem


class BackGroundPageElement(LayoutItem):
    def __init__(self, dom, parent_element, mxd, arc_doc):
        """
        This function creates the BackGroundPageElement
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, None, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_symbol(self):
        """
        The original QGIS File has a Symbol connected to the background 
        - remember this if errors occur or somebody needs a background thats not white... 
        """
        pass

    def create_background_layout_item(self):
        """
        This creates the background specific item content
        :return: 
        """
        layout_units = dict_units[self.arc_doc.PageLayout.Page.Units]
        bounds = self.arc_doc.PageLayout.Page.PrintableBounds

        back_ground_size = "{},{},{}".format(bounds.Width, bounds.Height, layout_units)

        basic_element = LayoutItem.create_layout_item_basic(self)
        LayoutItem.create_frame_element(self, basic_element)
        LayoutItem.create_background_element(self, basic_element)

        basic_element.setAttribute("size", back_ground_size)
        basic_element.setAttribute("frame", "false")
        basic_element.setAttribute("outlineWidthM", "0.3,{units}".format(units=layout_units))
        basic_element.setAttribute("positionOnPage", "0,0,{units}".format(units=layout_units))
        basic_element.setAttribute("position", "0,0,{units}".format(units=layout_units))

        basic_element.setAttribute("templateUuid", "{af5f0d73-7e44-42df-93ee-adea0eac5f05}")
        basic_element.setAttribute("uuid", "{af5f0d73-7e44-42df-93ee-adea0eac5f05}")
        basic_element.setAttribute("type", "65638")

        basic_element.setAttribute("groupUuid", "")
        basic_element.setAttribute("frameJoinStyle", "miter")


