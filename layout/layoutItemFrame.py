from layoutUuidProvider import LayoutUuidProvider
from layoutItem import LayoutItem
from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface


class LayoutItemFrame(LayoutItem):

    def __init__(self, dom, parent_element, map_object, mxd, arc_doc):
        """
        This function creates a frame(Map)-item 
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param map_object: The Map item as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, map_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.map_object = map_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_map_content(self, layout_item_base_element):
        """
        This function creats the frame-item specific content
        :param layout_item_base_element: the layout element in the DOM
        """
        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.layout_item_object)
        LayoutItemFrame.set_size_and_position(self, layout_item_base_element, arcpy_item)
        frame_properties = change_interface(self.map_object, ArcGisModules.module_carto.IFrameProperties)

        border = frame_properties.Border
        background = frame_properties.Background
        LayoutItemFrame.create_background_and_frame(self, border, background, layout_item_base_element)

        layout_item_base_element.setAttribute("type", "65639")
        layout_item_base_element.setAttribute("marginX", "0")
        layout_item_base_element.setAttribute("marginY", "0")
        layout_item_base_element.setAttribute("excludeFromExports", "0")
        layout_item_base_element.setAttribute("drawCanvasItems", "true")
        layout_item_base_element.setAttribute("rotation", unicode(arcpy_item.rotation))

        if self.layout_item_object.Map.Name not in LayoutUuidProvider.uuid_dict:
            LayoutUuidProvider.create_uuid(self.layout_item_object.Map.Name)
        uuid = unicode(LayoutUuidProvider.uuid_dict[self.layout_item_object.Map.Name])
        layout_item_base_element.setAttribute("uuid", uuid)
        layout_item_base_element.setAttribute("templateUuid", uuid)

        layout_item_base_element.setAttribute("followPreset", 'true')
        layout_item_base_element.setAttribute("followPresetName", arcpy_item.name)

        extent_element = self.dom.createElement("Extent")
        extent_element.setAttribute('ymax', "{}".format(arcpy_item.extent.YMax))
        extent_element.setAttribute('ymin', "{}".format(arcpy_item.extent.YMin))
        extent_element.setAttribute('xmax', "{}".format(arcpy_item.extent.XMax))
        extent_element.setAttribute('xmin', "{}".format(arcpy_item.extent.XMin))
        layout_item_base_element.appendChild(extent_element)

