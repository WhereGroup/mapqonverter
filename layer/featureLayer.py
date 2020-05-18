import arcpy
from renderer.renderer import Renderer as rendererObj
from renderer.labelRenderer import LabelRenderer


class FeatureLayer:

    def __init__(self):
        pass

    @staticmethod
    def create_feature_layer_content(base, map_layer_element):
        """ This Function creates Feature-layer specific content in the
            fitting maplayer-element

        :param base: Is the self from the LayerObject
        :param map_layer_element: the maplayer_element in the DOM
        """
        # logging.info('Feature Layer saved')
        geometry1 = arcpy.Describe(base.layer)
        geometry2 = str(geometry1.shapeType)
        map_layer_element.setAttribute("type", "vector")
        map_layer_element.setAttribute("geometry", geometry2)

        for datasource, provider in zip(map_layer_element.getElementsByTagName('datasource'),
                                        map_layer_element.getElementsByTagName('provider')):
            provider.setAttribute("encoding", "UTF-8")
            provider.appendChild(base.xml_document.createTextNode("ogr"))
            datasource.appendChild(base.xml_document.createTextNode(base.layer.dataSource))
            if len(base.layer.definitionQuery) > 0:
                datasource.firstChild.nodeValue = datasource.firstChild.nodeValue + "|layerid=0|subset=" \
                                                  + base.layer.definitionQuery

        renderer = rendererObj(base.xml_document, map_layer_element, base.arc_layer, base.layer, "feature")
        renderer.get_renderer()

        if base.layer.showLabels:
            for labelClass in base.layer.labelClasses:
                if labelClass.showClassLabels:
                    LabelRenderer.create_labels(
                        base,
                        map_layer_element,
                        label_dict=LabelRenderer.get_label_dict(
                            renderer,
                            renderer_type='feature'
                        )
                    )
            arcpy.AddWarning(
                "\t\tLabels have been converted. Complex Labeling is not supported. Check QGIS-File for result!"
            )
