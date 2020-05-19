class MapLegend:

    def __init__(self):
        pass

    @staticmethod
    def create_map_legend_element(xml_document, header, layerlist, dataframe):
        """ Creates the map-legend in the DOM

        :param xml_document: the document / DOM where all the information is saved
        :param header: the header of the DOM
        :param layerlist: the list of layers in the Dataframe
        :param dataframe: the dataframe
        """
        # there could be already a legend element if you have multiple dataframes
        legend_elements = xml_document.getElementsByTagName('legend')
        if len(legend_elements) == 0:
            legend_element = xml_document.createElement("legend")
            header.appendChild(legend_element)
        else:
            legend_element = xml_document.getElementsByTagName("legend")[0]

        dataframe_group_layer = xml_document.createElement("legendgroup")
        dataframe_group_layer.setAttribute("name", str(dataframe.name))
        dataframe_group_layer.setAttribute("checked", "Qt::Checked")
        dataframe_group_layer.setAttribute("open", "true")
        legend_element.appendChild(dataframe_group_layer)
        legendgroup = {}
        for layer in layerlist:
            # 2 (or more) grouplayer cant have the same name, if they are in the same branch and direct neighbours, sad
            if layer.isGroupLayer:
                MapLegend.create_group_layer_element(legendgroup, xml_document, layer, dataframe_group_layer)
            else:
                MapLegend.create_legend_layer_element(legendgroup, xml_document, layer, dataframe_group_layer)

    @staticmethod
    def create_group_layer_element(legendgroup, xml_document, layer, dataframe_group_layer):
        """ This creates a legend-group-layer element in the DOM

        :param legendgroup: a dictionary of legendgroup layers
        :param xml_document: the document / DOM where all the information is saved
        :param layer: the layer its about
        :param dataframe_group_layer: the dataframe_group_layer element in the DOM
        """
        legendgroup[layer.name] = xml_document.createElement("legendgroup")
        legendgroup[layer.name].setAttribute("name", layer.name)
        if layer.visible:
            legendgroup[layer.name].setAttribute("checked", "Qt::Checked")
        else:
            legendgroup[layer.name].setAttribute("checked", "Qt::Unchecked")
        legendgroup[layer.name].setAttribute("open", "true")
        # check long name for forgoing layers, append if exists, otherwise add to legend
        try:
            legendgroup[layer.longName.split("\\")[-2]].appendChild(legendgroup[layer.name])
        except IndexError:
            dataframe_group_layer.appendChild(legendgroup[layer.name])

    @staticmethod
    def create_legend_layer_element(legendgroup, xml_document, layer, dataframe_group_layer):
        """ This creates a legend-layer element in the DOM

        :param legendgroup: a dictionary of legendgroup layers
        :param xml_document: the document / DOM where all the information is saved
        :param layer: the layer its about
        :param dataframe_group_layer: the dataframe_group_layer element in the DOM
        """
        legendlayer = xml_document.createElement("legendlayer")
        legendlayer.setAttribute("open", "false")
        if layer.visible:
            legendlayer.setAttribute("checked", "Qt::Checked")
        else:
            legendlayer.setAttribute("checked", "Qt::Unchecked")
        legendlayer.setAttribute("name", layer.name)
        # same as for grouplayer-elements
        try:
            legendgroup[layer.longName.split("\\")[-2]].appendChild(legendlayer)
        except IndexError:
            dataframe_group_layer.appendChild(legendlayer)

        filegroup_element = xml_document.createElement("filegroup")
        filegroup_element.setAttribute("open", "false")
        filegroup_element.setAttribute("hidden", "false")
        legendlayer.appendChild(filegroup_element)

        legendlayer_file_element = xml_document.createElement("legendlayerfile")
        legendlayer_file_element.setAttribute("isInOverview", "0")
        legendlayer_file_element.setAttribute("layerid",  "{name}20190727170816078".format(name=layer.longName))
        legendlayer_file_element.setAttribute("visible", str(int(layer.visible)))
        filegroup_element.appendChild(legendlayer_file_element)
