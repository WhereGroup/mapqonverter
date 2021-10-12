class GdbFilePathProvider:
    def __init__(self):
        pass
    
    @staticmethod
    def create_layer_path_from_gdb_path(gdb_path):
        geo_data_base_name = gdb_path.split("\\")[-2]
        geo_data_base_path = gdb_path.split(geo_data_base_name)[0]
        geo_data_base_layer_name = gdb_path.split("\\")[-1]
        
        return geo_data_base_path + geo_data_base_name + "|layername=" + geo_data_base_layer_name
