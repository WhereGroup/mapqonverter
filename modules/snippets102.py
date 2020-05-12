# get_lib_path() and type_cast_module() from 
# http://pierssen.com/arcgis10/python.htm
# ************************************************


def unpack2rgb(rgb_long):
    """ This function converts a RGB-Long value to a Standard RGB-Code

    :param rgb_long: the RGB-Value as long
    :return: Standard RGB-Values as String 
    """
    red = rgb_long & 255
    green = (rgb_long >> 8) & 255
    blue = (rgb_long >> 16) & 255
    result = "{},{},{},255".format(str(red), str(green), str(blue))
    try:
        return result
    except (ValueError, Exception):
        return "255, 255, 255, 255"


def get_lib_path():
    """Return location of ArcGIS type libraries as string"""
    # This will still work on 64-bit machines because Python runs in 32 bit mode
    import _winreg
    key_esri = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\ESRI\\Desktop10.7")
    return _winreg.QueryValueEx(key_esri, "InstallDir")[0] + "com\\"


def type_cast_module(obj, interface):
    """Casts obj to interface and returns comtypes POINTER or None"""
    try:
        newobj = obj.QueryInterface(interface)
        return newobj
    except (ValueError, Exception):
        return None
