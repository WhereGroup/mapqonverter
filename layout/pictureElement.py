from layoutItem import LayoutItem
from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface


class PictureElement(LayoutItem):

    def __init__(self, dom, parent_element, picture_object, mxd, arc_doc):
        """
        This function creates a Picture-Item for the layout
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param picture_object: the picture_object as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, picture_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.picture_object = picture_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_picture_content(self, picture_element_base_layout):
        """
        This function creats the Picture-item specific content
        :param picture_element_base_layout: the layout element in the DOM
        """
        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.picture_object)
        PictureElement.set_size_and_position(self, picture_element_base_layout, arcpy_item)

        frame_properties = change_interface(self.picture_object, ArcGisModules.module_carto.IFrameProperties)

        border = frame_properties.Border
        background = frame_properties.Background
        PictureElement.create_background_and_frame(self, border, background, picture_element_base_layout)

        PictureElement.set_uuid_attributes(arcpy_item.name, picture_element_base_layout)
        picture_element_base_layout.setAttribute('type', "65640")
        picture_element_base_layout.setAttribute('file', arcpy_item.sourceImage.replace('\\', '/'))
