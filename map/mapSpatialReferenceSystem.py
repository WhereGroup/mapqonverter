from map.mapCanvas import MapCanvas
from spatialreferencesystem import SpatialReferenceSystem
import dictionaries.dict_arcgis_qgis as dict_arc_gis_qgis
from modules.srsReader import SrsReader


class MapSpatialReferenceSystem:
    def __init__(self):
        pass

    @staticmethod
    def create_map_srs_element(dom, header, dataframe):
        """ Create the map SRS element in the DOM

        :param dom: the document / DOM where all the information is saved
        :param header: the header of the DOM
        :param dataframe: the dataframe we are in
        """
        project_srs_element = dom.createElement("projectCrs")
        header.appendChild(project_srs_element)

        srs_input = SrsReader.get_srs_values(dataframe.spatialReference)

        spatialrefsys = SpatialReferenceSystem(
            srs_input['layerProj4'],
            srs_input['layerSrsid'],
            srs_input['layerSrid'],
            srs_input['layerAuth'],
            srs_input['layerDescription'],
            srs_input['layerEllipsoidacronym'],
            srs_input['layerProjectionacronym'],
            srs_input['layerGeographic']
        ).create_spatialrefsys(dom, project_srs_element)

        # create variables for mapcanvas and the element itself
        try:
            unit = dict_arc_gis_qgis.units[dataframe.mapUnits]
        except KeyError:
            unit = "degrees"
        rotation = int(dataframe.rotation)
        extent = [dataframe.extent.lowerLeft.X, dataframe.extent.lowerLeft.Y,
                  dataframe.extent.upperRight.X, dataframe.extent.upperRight.Y]

        MapCanvas(rotation, extent, unit, spatialrefsys.cloneNode(deep=True)).create_map_canvas(dom, header)
