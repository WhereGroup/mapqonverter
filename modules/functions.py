import winreg


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


def get_arc_object_library_path():
    """This function finds ArcMap in the registry and returns the Path to the arcObject-libraries-folder

    :return: The path to the ArcObject-libraries
    """
    path_to_arc_objects = ""
    for version_number in range(8, 3, -1):
        try:
            esri_hkey = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                "SOFTWARE\\ESRI\\Desktop10.{version_number}".format(version_number=version_number)
            )
            path_to_arc_objects = winreg.QueryValueEx(esri_hkey, "InstallDir")[0] + "com\\"
            break
        except WindowsError:
            pass

    return path_to_arc_objects


def type_cast_arc_object(arc_object, arc_interface):
    """This function casts an arc_object to an other interface and returns it

    :param arc_object: The arc_object to cast
    :param arc_interface: the interface to cast to
    :return: the new object or none
    """
    try:
        new_object = arc_object.QueryInterface(arc_interface)
    except (ValueError, Exception):
        new_object = None

    return new_object
