from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface


class Metadata:
    def __init__(self):
        pass

    @staticmethod
    def create_metadata(xml_document, header, arc_app):
        arc_doc = change_interface(arc_app.Item(0).Document, ArcGisModules.module_carto.IDocumentInfo2)

        project_metadata = xml_document.createElement('projectMetadata')
        header.appendChild(project_metadata)

        project_title = xml_document.createElement('title')
        project_title_content = xml_document.createTextNode(arc_doc.Name)
        project_title.appendChild(project_title_content)
        project_metadata.appendChild(project_title)

        project_author = xml_document.createElement('author')
        project_author_content = xml_document.createTextNode(arc_doc.Author)
        project_author.appendChild(project_author_content)
        project_metadata.appendChild(project_author)

        project_author = xml_document.createElement('abstract')
        project_author_content = xml_document.createTextNode(arc_doc.Subject)
        project_author.appendChild(project_author_content)
        project_metadata.appendChild(project_author)
