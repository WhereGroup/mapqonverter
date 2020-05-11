import arcpy

from renderer.labelRenderer import LabelRenderer
from renderer.renderer import Renderer as rendererObj


class DatabaseLayer:

    def __init__(self):
        pass

    @staticmethod
    def create_database_layer_content(base, map_layer_element):
        """ This Function creates database-layer specific content in the
            fitting maplayer-element

        :param base: Is the self from the LayerObject
        :param map_layer_element: the maplayer_element in the DOM
        """
        if "postgres" in base.layer.serviceProperties.get('Service', 'N/A'):
            provider_typ = "postgres"
        else:
            provider_typ = base.layer.serviceProperties.get('Service', 'N/A').split(":")[1]
        port = base.layer.serviceProperties.get('Service', 'N/A').split(", ")[1]
        db_name = base.layer.serviceProperties.get('Database', 'N/A')
        host = base.layer.serviceProperties.get('Server', 'N/A')
        description = arcpy.Describe(base.layer)
        geometry = str(description.shapeType)
        query = base.layer.definitionQuery
        # print self.lyr.definitionQuery
        table = "'" + base.layer.longName.split(".")[1] + "'.'" + base.layer.longName.split(".")[2] + "'"
        map_layer_element.setAttribute("type", "vector")
        map_layer_element.setAttribute("geometry", geometry)

        for data_source, provider in zip(map_layer_element.getElementsByTagName('datasource'),
                                         map_layer_element.getElementsByTagName('provider')):
            provider.setAttribute("encoding", "UTF-8")
            provider.appendChild(base.document.createTextNode(provider_typ))
            datasource_content = base.document.createTextNode("dbname='" + db_name +
                                                              "' host=" + host +
                                                              " port=" + port +
                                                              " sslmode=disable" +
                                                              " key='" + description.OIDFieldName +
                                                              "' type=" + geometry +
                                                              " srid=" + str(description.Spatialreference.GCSCode) +
                                                              " table=" + table +
                                                              " (geom) sql=" + query)
            data_source.appendChild(datasource_content)

        renderer = rendererObj(base.document, map_layer_element, base.arc_layer, base.layer, "feature")
        renderer.get_renderer()

        if base.layer.showLabels:
            for lblClass in base.layer.labelClasses:
                if lblClass.showClassLabels:
                    LabelRenderer.create_labels(base, map_layer_element, LabelRenderer.get_label_dict(base, "feature"))
            arcpy.AddWarning(
                "\t\tLabels have been converted. Complex Labeling is not supported. Check QGIS-File for result!"
            )
