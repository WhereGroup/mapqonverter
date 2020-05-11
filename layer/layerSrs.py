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
        if ".gdb" in base.gdb_path:
            annotation = {}
            # An Annotation has the SRS-Infos in the parent layer, also it can't be described without RuntimeError
            # Anyways it is possible with describe to get the needed informations in the annotation dictionary
            try:
                for parentLayer in base.layer_list:
                    if base.layer.longName.split("\\")[-2] == parentLayer.name:
                        description = arcpy.Describe(parentLayer).Spatialreference
                        annotation = SrsReader.get_srs_values(description)
                        break
                    else:
                        continue
            except RuntimeError:
                pass
            SpatialReferenceSystem(
                annotation['layerProj4'],
                annotation['layerSrsid'],
                annotation['layerSrid'],
                annotation['layerAuth'],
                annotation['layerDescription'],
                annotation['layerEllipsoidacronym'],
                annotation['layerProjectionacronym'],
                annotation['layerGeographic']
            ).create_spatialrefsys(base.document, srs_element)

        else:
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
                ).create_spatialrefsys(base.document, srs_element)

            except RuntimeError:
                # if crashes take, Project-srs
                spatialrefsys_element = base.document.getElementsByTagName('spatialrefsys')[0].cloneNode(deep=True)
                srs_element.appendChild(spatialrefsys_element)
                logging.info('Default SRS implemented, because of missing data')
