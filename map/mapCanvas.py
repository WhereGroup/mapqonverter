class MapCanvas:
    def __init__(self, rotation, extent, unit, spatialrefsys):
        self.rotation = rotation
        self.extent = extent
        self.unit = unit
        self.spatialrefsys = spatialrefsys

    def create_map_canvas(self, xml_document, header_element):
        """ Creates the mapCanvas Properties in the DOM

        :param xml_document: the document / DOM where all the information is saved
        :param header_element: the header element in the DOM
        :return:
        """

        mapcanvas_element = xml_document.createElement("mapcanvas")
        mapcanvas_element.setAttribute("name", "theMapCanvas")
        mapcanvas_element.setAttribute("annotationsVisible", "1")
        header_element.appendChild(mapcanvas_element)

        units_element = xml_document.createElement("units")
        units_content = xml_document.createTextNode(self.unit)
        units_element.appendChild(units_content)
        mapcanvas_element.appendChild(units_element)

        extent_element = xml_document.createElement("extent")
        mapcanvas_element.appendChild(extent_element)

        xmin_element = xml_document.createElement("xmin")
        xmin_content = xml_document.createTextNode(str(self.extent[0]))
        xmin_element.appendChild(xmin_content)
        extent_element.appendChild(xmin_element)

        ymin_element = xml_document.createElement("ymin")
        ymin_content = xml_document.createTextNode(str(self.extent[1]))
        ymin_element.appendChild(ymin_content)
        extent_element.appendChild(ymin_element)

        xmax_element = xml_document.createElement("xmax")
        xmax_content = xml_document.createTextNode(str(self.extent[2]))
        xmax_element.appendChild(xmax_content)
        extent_element.appendChild(xmax_element)

        ymax_element = xml_document.createElement("ymax")
        ymax_content = xml_document.createTextNode(str(self.extent[3]))
        ymax_element.appendChild(ymax_content)
        extent_element.appendChild(ymax_element)

        rotation_element = xml_document.createElement("rotation")
        rotation_content = xml_document.createTextNode(str(self.rotation))
        rotation_element.appendChild(rotation_content)
        mapcanvas_element.appendChild(rotation_element)

        destination_srs_element = xml_document.createElement("destinationsrs")
        mapcanvas_element.appendChild(destination_srs_element)

        spatialrefsys_element = self.spatialrefsys
        destination_srs_element.appendChild(spatialrefsys_element)

        render_maptile_element = xml_document.createElement("rendermaptile")
        render_maptile_content = xml_document.createTextNode("0")
        render_maptile_element.appendChild(render_maptile_content)
        mapcanvas_element.appendChild(render_maptile_element)

        return mapcanvas_element
