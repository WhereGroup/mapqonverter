import codecs
import xml
from xml.dom.minidom import Document, Node
import arcpy
from comtypes.client import CreateObject

from styleGalleryExport.CheckIfStyleFileIsAlreadyInStorageService import CheckIfStyleFileIsAlreadyInStorageService
from styleGalleryExport.ColorRampCreator import ColorRampCreator
from styleGalleryExport.LabelSettingsCreator import LabelSettingsCreator
from styleGalleryExport.SymbolCreator import SymbolCreator
from styleGalleryExport.TextFormatCreator import TextFormatCreator
from modules.functions import change_interface
from modules.arcGisModules import ArcGisModules


def main():
    """ This function converts a style gallery to XML"""
    style_file_path = arcpy.GetParameterAsText(0)
    export_name_path = arcpy.GetParameterAsText(1)
    classes_to_export = arcpy.GetParameter(2)

    arcpy.AddMessage("Start Processing...")

    style_gallery = CreateObject(ArcGisModules.module_framework.StyleGallery,
                                 interface=ArcGisModules.module_display.IStyleGallery
                                 )

    storage = change_interface(style_gallery, ArcGisModules.module_display.IStyleGalleryStorage)
    style_file_service = CheckIfStyleFileIsAlreadyInStorageService()

    if storage.DefaultStylePath in style_file_path:
        style_gallery_name = style_file_path.replace(storage.DefaultStylePath, "")
    else:
        style_gallery_name = style_file_path
    style_file_service.check_style_file(storage, style_gallery_name)

    if not style_file_service.style_file_exists_in_storage:
        storage.AddFile(style_file_path)

    qgis_style_xml = codecs.open(export_name_path, "w", encoding="utf-8")

    xml_document = Document()

    root_element = xml_document.createElement("qgis_style")
    root_element.setAttribute("version", "2")
    xml_document.appendChild(root_element)

    for class_to_export in classes_to_export:
        if class_to_export in [u'Marker Symbols', u'Fill Symbols', u'Line Symbols']:
            SymbolCreator(xml_document).create_symbols(style_gallery,
                                                       style_gallery_name,
                                                       class_to_export)
        elif class_to_export == u'Color Ramps':
            ColorRampCreator(xml_document).create_colorramps(style_gallery, style_gallery_name)
        elif class_to_export == u'Text Symbols':
            TextFormatCreator(xml_document).create_text_formats(style_gallery, style_gallery_name)
        elif class_to_export == u'Labels':
            LabelSettingsCreator(xml_document).create_label_settings(style_gallery, style_gallery_name)

    if not style_file_service.style_file_exists_in_storage:
        storage.RemoveFile(style_file_path)

    try:
        xml_document.writexml(qgis_style_xml, indent="  ", addindent="  ", newl="\n", encoding="UTF-8")
        arcpy.AddMessage("Style File saved!")
    finally:
        qgis_style_xml.close()


def pretty_writexml(self, writer, indent="", addindent="", newline=""):
    """ This functions has fixed formatting for the created XML-File
    :param writer = the file to write to
    :param indent = current indentation
    :param addindent = indentation to add to higher levels
    :param newline = newline string
    """
    writer.write(indent+"<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        xml.dom.minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if self.firstChild.nodeType == Node.TEXT_NODE \
                and self.childNodes.length == 1:
            writer.write(">")
            xml.dom.minidom. _write_data(writer, self.firstChild.data)
            writer.write("</%s>%s" % (self.tagName, newline))
        else:
            writer.write(">%s" % newline)
            for node in self.childNodes:
                node.writexml(writer, indent + addindent, addindent, newline)
            writer.write("%s</%s>%s" % (indent, self.tagName, newline))
    else:
        writer.write("/>%s" % newline)


xml.dom.minidom.Element.writexml = pretty_writexml

if __name__ == "__main__":
    main()
