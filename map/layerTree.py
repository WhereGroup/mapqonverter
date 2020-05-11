class LayerTree:
    def __init__(self):
        pass

    @staticmethod
    def create_layertree(dom, header, layerlist, dataframe):
        """ Creates the Layertree in the DOM

        :param dom: the document / DOM where all the information is saved
        :param header: the header of the DOM
        :param layerlist: the list of layers in the Dataframe
        :param dataframe: the dataframe
        """
        layer_tree_first_group_element = dom.getElementsByTagName('layer-tree-group')

        if len(layer_tree_first_group_element) == 0:
            layer_tree_element = dom.createElement("layer-tree-group")
            custom_properties_element = dom.createElement("customproperties")
            layer_tree_element.appendChild(custom_properties_element)
            map_canvas_elements = header.childNodes[5]
            header.insertBefore(layer_tree_element, map_canvas_elements)
        else:
            layer_tree_element = dom.getElementsByTagName("layer-tree-group")[0]

        dataframe_to_group_layer_element = dom.createElement("layer-tree-group")
        dataframe_to_group_layer_element.setAttribute("name", str(dataframe.name))
        dataframe_to_group_layer_element.setAttribute("checked", "Qt::Checked")
        dataframe_to_group_layer_element.setAttribute("expanded", "1")
        custom_properties_element = dom.createElement("customproperties")
        dataframe_to_group_layer_element.appendChild(custom_properties_element)
        layer_tree_element.appendChild(dataframe_to_group_layer_element)

        layer_tree_group = {}
        map_layer_count = 0
        for index, layer in enumerate(layerlist):
            # 2 (or more) grouplayer cant have the same name, if they are in the same branch and direct neighbours, sad
            if layer.isGroupLayer:
                layer_tree_group[layer.name] = dom.createElement("layer-tree-group")
                layer_tree_group[layer.name].setAttribute("name", layer.name)
                if layer.visible:
                    layer_tree_group[layer.name].setAttribute("checked", "Qt::Checked")
                else:
                    layer_tree_group[layer.name].setAttribute("checked", "Qt::Unchecked")
                layer_tree_group[layer.name].setAttribute("expanded", "1")
                # check long name for forgoing layers, append if exists, otherwise add to layer_tree_
                try:
                    layer_tree_group[layer.longName.split("\\")[-2]].appendChild(layer_tree_group[layer.name])
                except IndexError:
                    dataframe_to_group_layer_element.appendChild(layer_tree_group[layer.name])
                custom_properties_element = dom.createElement("customproperties")
                layer_tree_group[layer.name].appendChild(custom_properties_element)
            else:
                layer_tree_layer = dom.createElement("layer-tree-layer")

                if layer.supports('DATASOURCE'):
                    layer_tree_element_source = layer.dataSource
                    layer_tree_layer.setAttribute("source", layer_tree_element_source)

                if layer.visible:
                    layer_tree_layer.setAttribute("checked", "Qt::Checked")
                else:
                    layer_tree_layer.setAttribute("checked", "Qt::Unchecked")

                layer_tree_layer.setAttribute("name", layer.name)

                layer_tree_layer.setAttribute("id", layer.longName + str(20190727170816078))

                layer_tree_layer.setAttribute("expanded", "0")

                maplayer_elements = dom.getElementsByTagName('maplayer')[map_layer_count]
                provider_value = maplayer_elements.getElementsByTagName('provider')[0].firstChild.nodeValue
                layer_tree_layer.setAttribute("providerKey", provider_value)
                map_layer_count += 1

                # same as for grouplayer-elements
                try:
                    layer_tree_group[layer.longName.split("\\")[-2]].appendChild(layer_tree_layer)
                except IndexError:
                    dataframe_to_group_layer_element.appendChild(layer_tree_layer)

                custom_properties_element = dom.createElement("customproperties")
                layer_tree_layer.appendChild(custom_properties_element)

        custom_order_element = dom.createElement("custom-order")
        custom_order_element.setAttribute("enabled", "0")
        layer_tree_element.appendChild(custom_order_element)
