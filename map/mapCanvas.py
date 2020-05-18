class MapCanvas:
    def __init__(self, rotation, extent, unit, spatialrefsys):
        self.rotation = rotation
        self.extent = extent
        self.unit = unit
        self.spatialrefsys = spatialrefsys

    def create_map_canvas(self, dom, header_element):
        """ Creates the mapCanvas Properties in the DOM

        :param dom: the document / DOM where all the information is saved
        :param header_element: the header element in the DOM
        :return:
        """

        mapcanvas_element = dom.createElement("mapcanvas")
        mapcanvas_element.setAttribute("name", "theMapCanvas")
        mapcanvas_element.setAttribute("annotationsVisible", "1")
        header_element.appendChild(mapcanvas_element)

        units_element = dom.createElement("units")
        units_content = dom.createTextNode(self.unit)
        units_element.appendChild(units_content)
        mapcanvas_element.appendChild(units_element)

        extent_element = dom.createElement("extent")
        mapcanvas_element.appendChild(extent_element)

        xmin_element = dom.createElement("xmin")
        xmin_content = dom.createTextNode(str(self.extent[0]))
        xmin_element.appendChild(xmin_content)
        extent_element.appendChild(xmin_element)

        ymin_element = dom.createElement("ymin")
        ymin_content = dom.createTextNode(str(self.extent[1]))
        ymin_element.appendChild(ymin_content)
        extent_element.appendChild(ymin_element)

        xmax_element = dom.createElement("xmax")
        xmax_content = dom.createTextNode(str(self.extent[2]))
        xmax_element.appendChild(xmax_content)
        extent_element.appendChild(xmax_element)

        ymax_element = dom.createElement("ymax")
        ymax_content = dom.createTextNode(str(self.extent[3]))
        ymax_element.appendChild(ymax_content)
        extent_element.appendChild(ymax_element)

        rotation_element = dom.createElement("rotation")
        rotation_content = dom.createTextNode(str(self.rotation))
        rotation_element.appendChild(rotation_content)
        mapcanvas_element.appendChild(rotation_element)

        destination_srs_element = dom.createElement("destinationsrs")
        mapcanvas_element.appendChild(destination_srs_element)

        spatialrefsys_element = self.spatialrefsys
        destination_srs_element.appendChild(spatialrefsys_element)

        render_maptile_element = dom.createElement("rendermaptile")
        render_maptile_content = dom.createTextNode("0")
        render_maptile_element.appendChild(render_maptile_content)
        mapcanvas_element.appendChild(render_maptile_element)

        return mapcanvas_element
