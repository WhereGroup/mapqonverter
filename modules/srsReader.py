import re
from epsgToProj4Service import EpsgToProj4Service


class SrsReader:
    def __init__(self):
        pass

    @staticmethod
    def get_srs_values(spatialreference):
        """ Convert a SRS-Object to a SRS-Dictionary

        :param spatialreference: the SRS-Object to inspect
        :return: the SRS properties as a dictionary
        """
        srs_values = {
            'epsg': spatialreference.factoryCode,
            'layerDescription': spatialreference.name,
            'layerSrid': str(spatialreference.GCSCode),
            'layerGeographic': str(not spatialreference.PCSCode > 0)
        }

        srs_values['layerAuth'] = "EPSG:" + str(srs_values['epsg'])

        srs_values['layerProj4'] = EpsgToProj4Service.get_proj4_from_epsg_code(srs_values['epsg'])

        if "ellps" in srs_values['layerProj4']:
            proj4 = srs_values['layerProj4']
            found = re.search(r'ellps=(.+?)\s\+', proj4).group(1)
            srs_values['layerEllipsoidacronym'] = found.strip()
        else:
            srs_values['layerEllipsoidacronym'] = ""

        srs_values['layerProjectionacronym'] = "longlat"
        srs_values['layerSrsid'] = ""

        return srs_values

