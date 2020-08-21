from dictionaries.layoutItemsDict import dict_units


class UnitProvider:
    original_unit = None

    def __init__(self):
        pass

    @staticmethod
    def set_origin_unit(unit):
        UnitProvider.original_unit = unit

    @staticmethod
    def get_origin_unit():
        if not UnitProvider.original_unit:
            UnitProvider.original_unit = 7
        return UnitProvider.original_unit

    @staticmethod
    def get_unit_conversion_factor():

        unit_factor_dict = {'MM': 1, 'CM': 10, 'In': 25.4, 'Pt': 0.35278}

        origin_unit = dict_units[UnitProvider.get_origin_unit()]

        return unit_factor_dict[origin_unit]
