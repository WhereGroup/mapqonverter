from comtypes.client import GetModule
from snippets102 import get_lib_path


class ArcGisModules:
    """This class loads the ArcObject librarys as variables"""
    def __init__(self):
        pass

    module_carto = GetModule(get_lib_path() + "esriCarto.olb")
    module_display = GetModule(get_lib_path() + "esriDisplay.olb")
    module_gdb = GetModule(get_lib_path() + "esriGeoDatabase.olb")
    module_data_source_raster = GetModule(get_lib_path() + "esriDataSourcesRaster.olb")
    module_framework = GetModule(get_lib_path() + "esriFramework.olb")
    module_map_ui = GetModule(get_lib_path() + "esriArcMapUI.olb")
