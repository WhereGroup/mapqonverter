# Snippets.py
# ************************************************
# Updated for ArcGIS 10.2
# ************************************************
# Requires installation of the comtypes package
# Available at: http://sourceforge.net/projects/comtypes/
# Once comtypes is installed, the following modifications
# need to be made for compatibility with ArcGIS 10.2:
# 1) Delete automation.pyc, automation.pyo, safearray.pyc, safearray.pyo
# 2) Edit automation.py
# 3) Add the following entry to the _ctype_to_vartype dictionary (line 794):
#    POINTER(BSTR): VT_BYREF|VT_BSTR,
# ************************************************


def unpack2rgb(rgb_long):
    """ This function converts a RGB-Long value to a Standard RGB-Code

    :param rgb_long: the RGB-Value as long
    :return:
    """
    red = rgb_long & 255
    green = (rgb_long >> 8) & 255
    blue = (rgb_long >> 16) & 255
    result = "{},{},{},255".format(str(red), str(green), str(blue))
    try:
        return result
    except (ValueError, Exception):
        return "255", "255", "255", "255"


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
