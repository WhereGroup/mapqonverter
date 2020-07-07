from layoutUuidProvider import LayoutUuidProvider
from layoutItem import LayoutItem
from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_arc_object


class LegendElement(LayoutItem):

    def __init__(self, dom, parent_element, legend_object, mxd, arc_doc):
        """
        This function creates a legend-item
        :param dom: the Document Object Model
        :param parent_element: the main layout element, where to put the layout-items
        :param legend_object: the legend object as ArcObject
        :param mxd: the arcpy mxd-document
        :param arc_doc: the ArcObject IMxDocument
        """
        LayoutItem.__init__(self, dom, parent_element, legend_object, mxd, arc_doc)
        self.dom = dom
        self.parent_element = parent_element
        self.legend_object = legend_object
        self.mxd = mxd
        self.arc_doc = arc_doc

    def create_legend_content(self, layout_item_base_element):
        """
        This function creates the legend specific content
        :param layout_item_base_element: the layout element in the DOM
        """
        border = self.legend_object.Border

        background = self.legend_object.Background
        LegendElement.create_background_and_frame(self, border, background, layout_item_base_element)

        try:
            layout_item_base_element.setAttribute(
                'mapUuid',
                unicode(LayoutUuidProvider.uuid_dict[self.layout_item_object.MapSurround.Map.Name])
            )
        except KeyError:
            LayoutUuidProvider.create_uuid(self.layout_item_object.MapSurround.Map.Name)
            layout_item_base_element.setAttribute('mapUuid', unicode(
                LayoutUuidProvider.uuid_dict[self.layout_item_object.MapSurround.Map.Name])
            )

        LegendElement.set_uuid_attributes(self.layout_item_object.MapSurround.Name, layout_item_base_element)

        layout_item_base_element.setAttribute('type', "65642")
        layout_item_base_element.setAttribute('legendFilterByAtlas', "0")
        layout_item_base_element.setAttribute('equalColumnWidth', "0")
        layout_item_base_element.setAttribute('resizeToContents', "1")

        arcpy_item = LayoutItem.get_arcpy_layout_element(self, self.layout_item_object)
        LegendElement.set_size_and_position(self, layout_item_base_element, arcpy_item)

        legend_frame = type_cast_arc_object(self.legend_object.MapSurround, ArcGisModules.module_carto.ILegend2)
        legend_format = legend_frame.Format

        if legend_format.ShowTitle:
            layout_item_base_element.setAttribute('title', legend_frame.Title)

        layout_item_base_element.setAttribute('symbolHeight', unicode(legend_format.DefaultPatchHeight / 2.835))
        layout_item_base_element.setAttribute('symbolWidth', unicode(legend_format.DefaultPatchWidth / 2.835))

        layout_item_base_element.setAttribute('columnSpace', unicode(legend_format.HorizontalItemGap / 2.835))
        if self.legend_object.Border:
            layout_item_base_element.setAttribute('boxSpace', unicode(self.legend_object.Border.Gap / 2.835))
        layout_item_base_element.setAttribute('lineSpace', unicode(legend_format.VerticalItemGap / 2.835))

        LegendElement.create_style_element(self, legend_format, legend_frame, layout_item_base_element)
        LegendElement.create_layer_tree_element(self, legend_frame, layout_item_base_element)

        column_count = 1
        for index in range(0, legend_frame.ItemCount):
            if legend_frame[index].NewColumn:
                column_count += 1
        layout_item_base_element.setAttribute('columnCount', unicode(column_count))

    def create_style_element(self, legend_format, legend_frame, layout_item_base_element):
        """
        This function creates the style-element for the used Fonts/Groups (Title and SymbolLabel)
        :param legend_format: the legend format interface as ArcObject
        :param legend_frame: the legend interface as ArcObject
        :param layout_item_base_element: the layout element in the DOM
        """

        style_dict = {'title': {
            'style': {},
            'styleFont': {},
        }, 'symbolLabel': {
            'style': {},
            'styleFont': {},
        }}

        style_dict['title']['style']['name'] = 'title'
        style_dict['title']['style']['marginBottom'] = legend_format.TitleGap / 2.835
        style_dict['title']['style']['alignment'] = 1
        style_dict['title']['styleFont']['description'] = LegendElement.get_label_font_description(
            legend_format.TitleSymbol)
        style_dict['title']['styleFont']['style'] = ""

        style_dict['symbolLabel']['style']['name'] = 'symbolLabel'
        style_dict['symbolLabel']['style']['marginLeft'] = legend_format.HorizontalPatchGap / 2.835
        style_dict['symbolLabel']['style']['marginTop'] = legend_format.VerticalPatchGap / 2.835
        style_dict['symbolLabel']['style']['alignment'] = 1
        style_dict['symbolLabel']['styleFont']['description'] = LegendElement.get_label_font_description(
            legend_frame[0].LayerNameSymbol
        )
        style_dict['symbolLabel']['styleFont']['style'] = ""

        styles_element = self.dom.createElement('styles')
        layout_item_base_element.appendChild(styles_element)

        for keys in style_dict.iterkeys():
            style_element = self.dom.createElement('style')

            for key, value in style_dict[keys]['style'].iteritems():
                style_element.setAttribute(key, unicode(value))

            style_font_element = self.dom.createElement('styleFont')

            for key, value in style_dict[keys]['styleFont'].iteritems():
                style_font_element.setAttribute(key, unicode(value))

            style_element.appendChild(style_font_element)
            styles_element.appendChild(style_element)

    def create_layer_tree_element(self, legend_frame, layout_item_base_element):
        """
        This creates the layertree for the layout. 
            It packs all grouplayers at the bottom 
            and deletes all unused layers 
            -> closest to ArcMap design
        :param legend_frame: the legend interface as ArcObject
        :param layout_item_base_element: the layout element in the DOM
        """
        layer_tree_group_element = self.dom.getElementsByTagName('layer-tree-group')[0].cloneNode(deep=True)

        legend_item_count = legend_frame.ItemCount

        legend_layer_list = []
        for index in range(0, legend_item_count):
            legend_layer_list.append(legend_frame[index].Layer.Name)

        property_element = self.dom.createElement('property')
        property_element.setAttribute('key', "legend/title-style")
        property_element.setAttribute('value', "hidden")
        for element in layer_tree_group_element.getElementsByTagName('layer-tree-group'):
            element.getElementsByTagName('customproperties')[0].appendChild(property_element.cloneNode(deep=True))

        for element in layer_tree_group_element.getElementsByTagName('layer-tree-layer'):
            if element.getAttribute('name') not in legend_layer_list:
                parent = element.parentNode
                parent.removeChild(element)
            else:
                order_position = legend_layer_list.index(element.getAttribute('name'))
                try:
                    layer_tree_group_element.insertBefore(element,
                                                          layer_tree_group_element.childNodes[order_position + 1])
                except KeyError:
                    layer_tree_group_element.insertBefore(element, layer_tree_group_element.lastChild)

        layout_item_base_element.appendChild(layer_tree_group_element)
