import csv
import os


class EpsgToProj4Service:
    def __init__(self):
        pass

    @staticmethod
    def get_proj4_from_epsg_code(epsg):
        """ This function converts a epsg code to a proj4 string

        :param epsg: the epsg code to transform
        :return: the proj4 string
        """
        script_dir = os.path.dirname(__file__)
        rel_path = "mapbender_srs.csv"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'rb') as csv_file:
            proj4 = ''
            reader = csv.DictReader(csv_file, delimiter=';', fieldnames=['index', 'epsg', 'name', 'proj4'])
            for row in reader:
                if row['epsg'] == 'EPSG:{}'.format(epsg):
                    proj4 = row['proj4']
        return proj4

