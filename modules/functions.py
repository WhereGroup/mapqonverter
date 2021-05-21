import _ctypes
import arcpy


def is_close(float1, float2, relative_tolerance=1e-9, absolute_tolerance=0.0):
    """ This is a comparison for floats and taken from Python 3.5

    :param float1: Float - Value 1
    :param float2: Float - Value 1
    :param relative_tolerance: the relative tolerance in nano
    :param absolute_tolerance: minimum absolute tolerance
    :return: boolean
    """
    return abs(float1 - float2) <= max(relative_tolerance * max(abs(float1), abs(float2)), absolute_tolerance)


def convert_rgb_string_to_hex(rgb_string):
    rgb_colors = rgb_string.split(",")
    return '#{:02x}{:02x}{:02x}'.format(int(rgb_colors[0]), int(rgb_colors[1]), int(rgb_colors[2]))

def convert_int_to_rgb_string(rgb_int):
    """ This function converts a RGB-Int value to a Standard RGB-String
        The Alpha Value is fixed.

    :param rgb_int: the RGB-Value as Integer
    :return: Standard RGB-Values as String 
    """
    red = rgb_int & 255
    green = (rgb_int >> 8) & 255
    blue = (rgb_int >> 16) & 255
    result = "{},{},{},255".format(str(red), str(green), str(blue))
    try:
        return result
    except (ValueError, Exception):
        return "255, 255, 255, 255"


def get_arc_object_library_path():
    """This function finds ArcMap in the registry and returns the Path to the arcObject-libraries-folder

    :return: The path to the ArcObject-libraries
    """
    install_directory = arcpy.GetInstallInfo()['InstallDir']
    lib_directory = '{install_dir}com\\'.format(install_dir=install_directory)

    return lib_directory


def change_interface(arc_object, new_interface):
    """This function changes an interface from an arcObject and returns it

    :param arc_object: The arc_object
    :param new_interface: the interface to use
    :return: the new interface or none
    """
    try:
        object_with_new_interface = arc_object.QueryInterface(new_interface)
    except (_ctypes.COMError, Exception):
        object_with_new_interface = None

    return object_with_new_interface
