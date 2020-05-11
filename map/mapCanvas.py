class MapCanvas:
    def __init__(self, rotation, extent, unit, spatialrefsys):
        self.rotation = rotation
        self.extent = extent
        self.unit = unit
        self.spatialrefsys = spatialrefsys

    def create_map_canvas(self, doc, qgis):
        """ Creates the mapCanvas Properties in the DOM

        :param doc: the document / DOM where all the information is saved
        :param qgis: the qgis element in the DOM
        :return:
        """

        mapcanvas_element = doc.createElement("mapcanvas")
        mapcanvas_element.setAttribute("name", "theMapCanvas")
        mapcanvas_element.setAttribute("annotationsVisible", "1")
        qgis.appendChild(mapcanvas_element)

        units_element = doc.createElement("units")
        units_content = doc.createTextNode(self.unit)
        units_element.appendChild(units_content)
        mapcanvas_element.appendChild(units_element)

        extent_element = doc.createElement("extent")
        mapcanvas_element.appendChild(extent_element)

        xmin_element = doc.createElement("xmin")
        xmin_content = doc.createTextNode(str(self.extent[0]))
        xmin_element.appendChild(xmin_content)
        extent_element.appendChild(xmin_element)

        ymin_element = doc.createElement("ymin")
        ymin_content = doc.createTextNode(str(self.extent[1]))
        ymin_element.appendChild(ymin_content)
        extent_element.appendChild(ymin_element)

        xmax_element = doc.createElement("xmax")
        xmax_content = doc.createTextNode(str(self.extent[2]))
        xmax_element.appendChild(xmax_content)
        extent_element.appendChild(xmax_element)

        ymax_element = doc.createElement("ymax")
        ymax_content = doc.createTextNode(str(self.extent[3]))
        ymax_element.appendChild(ymax_content)
        extent_element.appendChild(ymax_element)

        rotation_element = doc.createElement("rotation")
        rotation_content = doc.createTextNode(str(self.rotation))
        rotation_element.appendChild(rotation_content)
        mapcanvas_element.appendChild(rotation_element)

        destination_srs_element = doc.createElement("destinationsrs")
        mapcanvas_element.appendChild(destination_srs_element)

        spatialrefsys_element = self.spatialrefsys
        destination_srs_element.appendChild(spatialrefsys_element)

        render_maptile_element = doc.createElement("rendermaptile")
        render_maptile_content = doc.createTextNode("0")
        render_maptile_element.appendChild(render_maptile_content)
        mapcanvas_element.appendChild(render_maptile_element)

        return mapcanvas_element
