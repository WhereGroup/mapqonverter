class SpatialReferenceSystem:
    def __init__(self, proj4, srsid, srid, authid, description, ellipsoidacronym, projectionacronym, geographicflag):
        self.proj4 = proj4
        self.srsid = srsid
        self.srid = srid
        self.authid = authid
        self.description = description
        self.ellipsoidacronym = ellipsoidacronym
        self.projectionacronym = projectionacronym
        self.geographicflag = geographicflag

    def create_spatialrefsys(self, dom, project_crs):
        """ Creates the SRS_element for the DOM

        :param dom: The DOM / Document for writing the QGIS-File
        :param project_crs: the project_crs_element in the DOM
        :return: the spatial_ref_sys_element
        """
        spatial_ref_sys_element = dom.createElement("spatialrefsys")
        project_crs.appendChild(spatial_ref_sys_element)

        proj4_element = dom.createElement("proj4")
        proj4_content = dom.createTextNode(self.proj4)
        proj4_element.appendChild(proj4_content)
        spatial_ref_sys_element.appendChild(proj4_element)

        srsid_element = dom.createElement("srsid")
        srsid_content = dom.createTextNode(self.srsid)
        srsid_element.appendChild(srsid_content)
        spatial_ref_sys_element.appendChild(srsid_element)

        srid_element = dom.createElement("srid")
        srid_content = dom.createTextNode(self.srid)
        srid_element.appendChild(srid_content)
        spatial_ref_sys_element.appendChild(srid_element)

        authid_element = dom.createElement("authid")
        authid_content = dom.createTextNode(self.authid)
        authid_element.appendChild(authid_content)
        spatial_ref_sys_element.appendChild(authid_element)

        description_element = dom.createElement("description")
        description_content = dom.createTextNode(self.description)
        description_element.appendChild(description_content)
        spatial_ref_sys_element.appendChild(description_element)

        projectionacronym = dom.createElement("projectionacronym")
        content = dom.createTextNode(self.projectionacronym)
        projectionacronym.appendChild(content)
        spatial_ref_sys_element.appendChild(projectionacronym)

        ellipsoidacronym_element = dom.createElement("ellipsoidacronym")
        ellipsoidacronym_content = dom.createTextNode(self.ellipsoidacronym)
        ellipsoidacronym_element.appendChild(ellipsoidacronym_content)
        spatial_ref_sys_element.appendChild(ellipsoidacronym_element)

        geographicflag_element = dom.createElement("geographicflag")
        geographicflag_content = dom.createTextNode(self.geographicflag)
        geographicflag_element.appendChild(geographicflag_content)
        spatial_ref_sys_element.appendChild(geographicflag_element)

        return spatial_ref_sys_element
