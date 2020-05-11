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

    def create_spatialrefsys(self, doc, project_crs):
        """ Creates the SRS_element for the DOM

        :param doc: The DOM / Document for writing the QGIS-File
        :param project_crs: the project_crs_element in the DOM
        :return: the spatial_ref_sys_element
        """
        spatial_ref_sys_element = doc.createElement("spatialrefsys")
        project_crs.appendChild(spatial_ref_sys_element)

        proj4_element = doc.createElement("proj4")
        proj4_content = doc.createTextNode(self.proj4)
        proj4_element.appendChild(proj4_content)
        spatial_ref_sys_element.appendChild(proj4_element)

        srsid_element = doc.createElement("srsid")
        srsid_content = doc.createTextNode(self.srsid)
        srsid_element.appendChild(srsid_content)
        spatial_ref_sys_element.appendChild(srsid_element)

        srid_element = doc.createElement("srid")
        srid_content = doc.createTextNode(self.srid)
        srid_element.appendChild(srid_content)
        spatial_ref_sys_element.appendChild(srid_element)

        authid_element = doc.createElement("authid")
        authid_content = doc.createTextNode(self.authid)
        authid_element.appendChild(authid_content)
        spatial_ref_sys_element.appendChild(authid_element)

        # Create the <description> element
        description_element = doc.createElement("description")
        description_content = doc.createTextNode(self.description)
        description_element.appendChild(description_content)
        spatial_ref_sys_element.appendChild(description_element)

        # Create the <projectionacronym> element
        projectionacronym = doc.createElement("projectionacronym")
        content = doc.createTextNode(self.projectionacronym)
        projectionacronym.appendChild(content)
        spatial_ref_sys_element.appendChild(projectionacronym)

        # Create the <ellipsoidacronym element
        ellipsoidacronym_element = doc.createElement("ellipsoidacronym")
        ellipsoidacronym_content = doc.createTextNode(self.ellipsoidacronym)
        ellipsoidacronym_element.appendChild(ellipsoidacronym_content)
        spatial_ref_sys_element.appendChild(ellipsoidacronym_element)

        # Create the <geographicflag> element
        geographicflag_element = doc.createElement("geographicflag")
        geographicflag_content = doc.createTextNode(self.geographicflag)
        geographicflag_element.appendChild(geographicflag_content)
        spatial_ref_sys_element.appendChild(geographicflag_element)

        return spatial_ref_sys_element
