class MapProperties:

    def __init__(self):
        pass

    @staticmethod
    def create_map_properties_element(dom, header):
        """ This creates the map properties element in the DOM

        :param dom: the document / DOM where all the information is saved
        :param header: the header of the DOM
        """

        properties_element = dom.createElement("properties")
        header.appendChild(properties_element)

        position_precision_element = dom.createElement("PositionPrecision")
        properties_element.appendChild(position_precision_element)

        decimal_places_element = dom.createElement("DecimalPlaces")
        decimal_places_element.setAttribute("type", "int")
        decimal_places_element_content = dom.createTextNode("2")
        decimal_places_element.appendChild(decimal_places_element_content)
        position_precision_element.appendChild(decimal_places_element)

        automatic_element = dom.createElement("Automatic")
        automatic_element.setAttribute("type", "bool")
        automatic_element_content = dom.createTextNode("true")
        automatic_element.appendChild(automatic_element_content)
        position_precision_element.appendChild(automatic_element)

        measurement_element = dom.createElement("Measurement")
        properties_element.appendChild(measurement_element)

        distance_units_element = dom.createElement("DistanceUnits")
        distance_units_element.setAttribute("type", "QString")
        distance_units_element_content = dom.createTextNode("meters")
        distance_units_element.appendChild(distance_units_element_content)
        measurement_element.appendChild(distance_units_element)

        area_units_element = dom.createElement("AreaUnits")
        area_units_element.setAttribute("type", "QString")
        area_units_element_content = dom.createTextNode("m2")
        area_units_element.appendChild(area_units_element_content)
        measurement_element.appendChild(area_units_element)

        srs_element = dom.createElement("SpatialRefSys")
        properties_element.appendChild(srs_element)

        project_crs_proj4_string_element = dom.createElement("ProjectCRSProj4String")
        project_crs_proj4_string_element.setAttribute("type", "QString")
        proj4_content = dom.getElementsByTagName('proj4')[0].firstChild.nodeValue
        project_crs_proj4_string_element.appendChild(dom.createTextNode(proj4_content))
        srs_element.appendChild(project_crs_proj4_string_element)

        project_crsid_element = dom.createElement("ProjectCRSID")
        project_crsid_element.setAttribute("type", "int")
        srsid_content = dom.getElementsByTagName('srsid')[0].firstChild.nodeValue
        project_crsid_element.appendChild(dom.createTextNode(srsid_content))
        srs_element.appendChild(project_crsid_element)

        project_crs_element = dom.createElement("ProjectCrs")
        project_crs_element.setAttribute("type", "QString")
        authid_content = dom.getElementsByTagName('authid')[0].firstChild.nodeValue
        project_crs_element.appendChild(dom.createTextNode(authid_content))
        srs_element.appendChild(project_crs_element)

        rojections_enabled_element = dom.createElement("ProjectionsEnabled")
        rojections_enabled_element.setAttribute("type", "int")
        rojections_enabled_element.appendChild(dom.createTextNode("1"))
        srs_element.appendChild(rojections_enabled_element)

        measure_element = dom.createElement("Measure")
        properties_element.appendChild(measure_element)

        ellipsoidacronym_content = dom.getElementsByTagName('ellipsoidacronym')[0].firstChild.nodeValue
        ellipsoid_element = dom.createElement("Ellipsoid")
        ellipsoid_element.setAttribute("type", "QString")
        ellipsoid_element.appendChild(dom.createTextNode(ellipsoidacronym_content))
        measure_element.appendChild(ellipsoid_element)
