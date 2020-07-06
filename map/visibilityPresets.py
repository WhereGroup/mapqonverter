import arcpy


class VisibilityPresets:
    def __init__(self):
        pass

    @staticmethod
    def initialize_visibility(dom, header, mxd):

        visibility_base_element = VisibilityPresets.__create_visibility_presets_base(dom, header)

        for dataframe in arcpy.mapping.ListDataFrames(mxd):
            VisibilityPresets.__create_visibility_preset(dom, header, visibility_base_element, dataframe)

    @staticmethod
    def __create_visibility_presets_base(dom, header):
        visibility_presets_element = dom.createElement("visibility-presets")
        header.appendChild(visibility_presets_element)

        return visibility_presets_element

    @staticmethod
    def __create_visibility_preset(dom, header, visibility_base_element, dataframe):
        visibility_preset_element = dom.createElement("visibility-preset")
        visibility_preset_element.setAttribute('name', dataframe.name)
        visibility_preset_element.setAttribute('has-expanded-info', "1")
        visibility_preset_element.setAttribute('has-checked-group-info', "1")

        main_layer_tree_group_elements = header.getElementsByTagName('layer-tree-group')[0]

        inside_data_frame_layers = []
        outside_data_frame_layers = []

        for child_node in main_layer_tree_group_elements.childNodes:
            if child_node.nodeName == 'layer-tree-group' and child_node.getAttribute('name') == dataframe.name:
                inside_data_frame_layers = child_node.getElementsByTagName('layer-tree-layer')

            if child_node.nodeName == 'layer-tree-group' and not child_node.getAttribute('name') == dataframe.name:
                outside_data_frame_layers = child_node.getElementsByTagName('layer-tree-layer')

        all_layers = outside_data_frame_layers + inside_data_frame_layers

        for layer in all_layers:
            layer_element = dom.createElement('layer')
            layer_element.setAttribute('id', layer.getAttribute('id'))
            layer_element.setAttribute('expanded', '0')
            if layer in inside_data_frame_layers:
                layer_element.setAttribute('visible', '1' if layer.getAttribute('checked') == "Qt::Checked" else '0')
            else:
                layer_element.setAttribute('visible', '0')
            layer_element.setAttribute('style', "default")
            visibility_preset_element.appendChild(layer_element)

            expanded_legend_nodes_element = dom.createElement('expanded-legend-nodes')
            expanded_legend_nodes_element.setAttribute('id', layer.getAttribute('id'))
            visibility_preset_element.appendChild(expanded_legend_nodes_element)

        checked_group_nodes_element = dom.createElement('checked-group-nodes')
        expanded_group_nodes_element = dom.createElement('expanded-group-nodes')

        for layer in arcpy.mapping.ListLayers(dataframe):
            if layer.isGroupLayer:
                VisibilityPresets.create_group_node_specific_elements(
                    dom,
                    u"{}/{}".format(dataframe.name, layer.longName.replace('\\', '/')),
                    checked_group_nodes_element,
                    expanded_group_nodes_element
                )

        VisibilityPresets.create_group_node_specific_elements(
            dom, 
            dataframe.name, 
            checked_group_nodes_element, 
            expanded_group_nodes_element
        )

        visibility_preset_element.appendChild(checked_group_nodes_element)
        visibility_preset_element.appendChild(expanded_group_nodes_element)
        visibility_base_element.appendChild(visibility_preset_element)

    @staticmethod
    def create_group_node_specific_elements(dom, layer_name, checked_group_nodes_element, expanded_group_nodes_element):
        checked_group_node_element = dom.createElement('checked-group-node')
        checked_group_node_element.setAttribute('id', layer_name)
        checked_group_nodes_element.appendChild(checked_group_node_element)

        expanded_group_node_element = dom.createElement('expanded-group-node')
        expanded_group_node_element.setAttribute('id', layer_name)
        expanded_group_nodes_element.appendChild(expanded_group_node_element)







