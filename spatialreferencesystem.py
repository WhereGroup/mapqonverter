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

    def create_spatialrefsys(self, xml_document, project_crs):
        """ Creates the SRS_element for the DOM

        :param xml_document: The DOM / Document for writing the QGIS-File
        :param project_crs: the project_crs_element in the DOM
        :return: the spatial_ref_sys_element
        """
        spatial_ref_sys_element = xml_document.createElement("spatialrefsys")
        project_crs.appendChild(spatial_ref_sys_element)

        proj4_element = xml_document.createElement("proj4")
        proj4_content = xml_document.createTextNode(self.proj4)
        proj4_element.appendChild(proj4_content)
        spatial_ref_sys_element.appendChild(proj4_element)

        srsid_element = xml_document.createElement("srsid")
        srsid_content = xml_document.createTextNode(self.srsid)
        srsid_element.appendChild(srsid_content)
        spatial_ref_sys_element.appendChild(srsid_element)

        srid_element = xml_document.createElement("srid")
        srid_content = xml_document.createTextNode(self.srid)
        srid_element.appendChild(srid_content)
        spatial_ref_sys_element.appendChild(srid_element)

        authid_element = xml_document.createElement("authid")
        authid_content = xml_document.createTextNode(self.authid)
        authid_element.appendChild(authid_content)
        spatial_ref_sys_element.appendChild(authid_element)

        description_element = xml_document.createElement("description")
        description_content = xml_document.createTextNode(self.description)
        description_element.appendChild(description_content)
        spatial_ref_sys_element.appendChild(description_element)

        projectionacronym = xml_document.createElement("projectionacronym")
        content = xml_document.createTextNode(self.projectionacronym)
        projectionacronym.appendChild(content)
        spatial_ref_sys_element.appendChild(projectionacronym)

        ellipsoidacronym_element = xml_document.createElement("ellipsoidacronym")
        ellipsoidacronym_content = xml_document.createTextNode(self.ellipsoidacronym)
        ellipsoidacronym_element.appendChild(ellipsoidacronym_content)
        spatial_ref_sys_element.appendChild(ellipsoidacronym_element)

        geographicflag_element = xml_document.createElement("geographicflag")
        geographicflag_content = xml_document.createTextNode(self.geographicflag)
        geographicflag_element.appendChild(geographicflag_content)
        spatial_ref_sys_element.appendChild(geographicflag_element)

        return spatial_ref_sys_element
