from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface


class StyleGalleryItemProvider:
    def __init__(self):
        pass

    @staticmethod
    def get_style_gallery_items(style_gallery, item_type, style_gallery_name):
        """ This function reads the items of a given type out of the style-gallery and returns them.

        :param style_gallery: The Style-Gallery-Object -> IStyleGallery
        :param item_type: The Typ of the Item (for Example "Marker Symbols")
        :param style_gallery_name: The name of the style-gallery to export
        :return: list of StyleGalleryItems
        """
        items_iterator = style_gallery.Items(item_type, style_gallery_name, None)
        items_iterator.reset()

        items_list = []

        item = change_interface(items_iterator.next(), ArcGisModules.module_display.IStyleGalleryItem)
        while item is not None:
            items_list.append(item)
            item = change_interface(items_iterator.next(), ArcGisModules.module_display.IStyleGalleryItem)

        return items_list
