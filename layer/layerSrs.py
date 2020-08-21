import arcpy
from spatialreferencesystem import SpatialReferenceSystem
from modules.srsReader import SrsReader
import logging


class LayerSrs:
    def __init__(self):
        pass

    @staticmethod
    def create_layer_srs(base, srs_element):
        """ This Function creates the srs-specific content in the
            fitting maplayer-element

        :param base: Is the self from the LayerObject
        :param srs_element: the srs_element in the DOM
        """
        if ".gdb" in base.gdb_path and not base.layer.isFeatureLayer:
            LayerSrs.create_gdb_annotation_srs(base, srs_element)
        else:
            LayerSrs.create_normal_layer_srs(base, srs_element)

    @staticmethod
    def create_map_srs(base, srs_element):
        spatialrefsys_element = base.xml_document.getElementsByTagName('spatialrefsys')[0].cloneNode(deep=True)
        srs_element.appendChild(spatialrefsys_element)
        logging.info('Default SRS implemented, because of missing data')

    @staticmethod
    def create_gdb_annotation_srs(base, srs_element):
        annotation = {}
        # An Annotation has the SRS-Infos in the parent layer, also it can't be described without RuntimeError
        # Anyways it is possible with describe to get the needed informations in the annotation dictionary
        try:
            forgoing_layer = base.layer.longName.rsplit("\\", 1)[0]
            for parentLayer in base.layer_list:
                if forgoing_layer == parentLayer.longName:
                    description = arcpy.Describe(parentLayer).Spatialreference
                    annotation = SrsReader.get_srs_values(description)
                    break
                else:
                    continue
        except (RuntimeError, IndexError):
            pass
        if len(annotation) > 0:
            SpatialReferenceSystem(
                annotation['layerProj4'],
                annotation['layerSrsid'],
                annotation['layerSrid'],
                annotation['layerAuth'],
                annotation['layerDescription'],
                annotation['layerEllipsoidacronym'],
                annotation['layerProjectionacronym'],
                annotation['layerGeographic']
            ).create_spatialrefsys(base.xml_document, srs_element)
        else:
            LayerSrs.create_map_srs(base, srs_element)

    @staticmethod
    def create_normal_layer_srs(base, srs_element):
        try:
            description = arcpy.Describe(base.layer).Spatialreference

            srs_input = SrsReader.get_srs_values(description)

            SpatialReferenceSystem(
                srs_input['layerProj4'],
                srs_input['layerSrsid'],
                srs_input['layerSrid'],
                srs_input['layerAuth'],
                srs_input['layerDescription'],
                srs_input['layerEllipsoidacronym'],
                srs_input['layerProjectionacronym'],
                srs_input['layerGeographic']
            ).create_spatialrefsys(base.xml_document, srs_element)

        except RuntimeError:
            # if crashes take, Project-srs
            LayerSrs.create_map_srs(base, srs_element)
