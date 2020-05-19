from comtypes.client import GetModule
from functions import get_lib_path


class ArcGisModules:
    """This class loads the ArcObject librarys as variables"""
    def __init__(self):
        pass

    lib_path = get_lib_path()
    module_carto = GetModule("{lib_path}esriCarto.olb".format(lib_path=lib_path))
    module_display = GetModule("{lib_path}esriDisplay.olb".format(lib_path=lib_path))
    module_gdb = GetModule("{lib_path}esriGeoDatabase.olb".format(lib_path=lib_path))
    module_data_source_raster = GetModule("{lib_path}esriDataSourcesRaster.olb".format(lib_path=lib_path))
    module_framework = GetModule("{lib_path}esriFramework.olb".format(lib_path=lib_path))
    module_map_ui = GetModule("{lib_path}esriArcMapUI.olb".format(lib_path=lib_path))
