class ZValueProvider:
    number_of_elements = 0

    def __init__(self):
        pass

    @staticmethod
    def get_z_value():
        """
        This function returns the ZValue of an element.
        The value decreases for each element.
         
        The number of elements is set, when the layout elements have been collected in layout.py.
        """

        ZValueProvider.number_of_elements = ZValueProvider.number_of_elements - 1

        return unicode(ZValueProvider.number_of_elements)
