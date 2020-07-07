import random

from modules.functions import type_cast_arc_object, convert_int_to_rgb_string
from dictionaries.label_dict import labelDict
from modules.arcGisModules import ArcGisModules


class LabelRenderer:
    def __init__(self):
        pass

    @staticmethod
    def get_label_dict(base, renderer_type):
        """ This function collects all properties of the label and returns them as a dictionary

        :param base: the renderer-object
        :param renderer_type: the type of the used renderer
        :return: the label dictionary including all the label properties
        """
        symbol = None
        if renderer_type == "gdb":
            # first get annotation-parent-layer, here are the style infos for the fitting ClassId
            annotation_parent_layer = type_cast_arc_object(
                base.arcLayer,
                ArcGisModules.module_carto.IAnnotationSublayer).Parent
            annotation_class_id = type_cast_arc_object(
                base.arcLayer,
                ArcGisModules.module_carto.IAnnotationSublayer).AnnotationClassID
            # over the Class - Extension you get to the AnnotationClassExtension
            annotation_class = type_cast_arc_object(
                annotation_parent_layer,
                ArcGisModules.module_gdb.IClass)
            annotation_class_extension = type_cast_arc_object(
                annotation_class.Extension,
                ArcGisModules.module_carto.IAnnotationClassExtension
            )
            # and finally the right formatted symbol
            symbol = annotation_class_extension.SymbolCollection.Symbol[annotation_class_id]

            labelDict['labelValues']['type'] = 'rule-based'
            labelDict['labelValues']['classId'] = str(annotation_class_id)
            labelDict['labelValues']['text-style']['fieldName'] = 'TextString'
        elif renderer_type == "feature":
            # get the AnnotationProps, that lead to the Labelrenderer and the Symbol
            feature_layer = type_cast_arc_object(base.arcLayer, ArcGisModules.module_carto.IGeoFeatureLayer)
            annotation_parent_layer = type_cast_arc_object(
                feature_layer.AnnotationProperties,
                ArcGisModules.module_carto.IAnnotateLayerPropertiesCollection2
            )
            label_engine = type_cast_arc_object(
                annotation_parent_layer.Properties(0),
                ArcGisModules.module_carto.ILabelEngineLayerProperties2
            )
            if feature_layer.DisplayFeatureClass.ShapeType == 3:
                label_placement = '2'
            else:
                label_placement = '0'
            labelDict['labelValues']['placement']['placement'] = label_placement
            symbol = label_engine.Symbol
            expression = label_engine.Expression
            labelDict['labelValues']['type'] = 'simple'
            labelDict['labelValues']['text-style']['fieldName'] = expression[1:-1]
        formatted_symbol = type_cast_arc_object(symbol, ArcGisModules.module_display.IFormattedTextSymbol)
        # fill the values
        labelDict['labelValues']['placement']['rotationAngle'] = str(formatted_symbol.Angle)
        labelDict['labelValues']['text-style']['fontLetterSpacing'] = str(formatted_symbol.CharacterSpacing)
        # labelDict['labelValues']['text-style']['fontWordSpacing'] = str(formattedSymbol.WordSpacing)
        labelDict['labelValues']['text-style']['textColor'] = convert_int_to_rgb_string(formatted_symbol.Color.RGB)
        labelDict['labelValues']['text-style']['fontFamily'] = formatted_symbol.Font.Name
        labelDict['labelValues']['text-style']['fontWeight'] = str(formatted_symbol.Font.Weight)
        labelDict['labelValues']['text-style']['fontSize'] = str(formatted_symbol.Size)
        labelDict['labelValues']['text-style']['fontItalic'] = str(int(formatted_symbol.Font.Italic))
        labelDict['labelValues']['text-style']['fontUnderline'] = str(int(formatted_symbol.Font.Underline))
        try:
            formatted_symbol_callout = type_cast_arc_object(
                formatted_symbol.Background,
                ArcGisModules.module_display.ILineCallout
            )
            formatted_symbol_callout_margin = type_cast_arc_object(
                formatted_symbol.Background,
                ArcGisModules.module_display.ITextMargins
            )
            labelDict['labelValues']['background']['shapeFillColor'] = convert_int_to_rgb_string(
                formatted_symbol_callout.Border.Color.RGB
            )
            labelDict['labelValues']['background']['shapeBorderColor'] = convert_int_to_rgb_string(
                formatted_symbol_callout.Border.Outline.Color.RGB
            )
            labelDict['labelValues']['background']['shapeBorderWidth'] = str(
                formatted_symbol_callout.Border.Outline.Width
            )
            labelDict['labelValues']['background']['shapeSizeX'] = str(
                                                                    int(formatted_symbol_callout_margin.LeftMargin)*2
                                                                    )
            labelDict['labelValues']['background']['shapeSizeY'] = str(int(formatted_symbol_callout_margin.TopMargin)*2)
            labelDict['labelValues']['background']['shapeDraw'] = "1"
        except (AttributeError, ValueError):
            labelDict['labelValues']['background']['shapeDraw'] = "0"
            # print "Label has no Background"

        if formatted_symbol.Font.Bold:
            labelDict['labelValues']['text-style']['namedStyle'] = "Bold"
        else:
            labelDict['labelValues']['text-style']['namedStyle'] = "Standard"

        labelDict['labelValues']['shadow']['shadowColor'] = convert_int_to_rgb_string(formatted_symbol.ShadowColor.RGB)

        return labelDict

    @staticmethod
    def create_labels(base, map_layer_element, label_dict):
        """ This writes all the informations of a label in the maplayer_element in the DOM

        :param base: the renderer-object
        :param map_layer_element: the maplayer-element in the DOM
        :param label_dict: the label dictionary including all the label properties
        """
        labeling_element = base.xml_document.createElement("labeling")
        labeling_element.setAttribute("type", label_dict['labelValues']['type'])
        map_layer_element.appendChild(labeling_element)

        settings_element = base.xml_document.createElement("settings")

        if label_dict['labelValues']['type'] == 'rule-based':

            rules_element = base.xml_document.createElement("rules")
            rules_element.setAttribute("key", "{a5f41347-c300-4ee5-b" + str(random.randint(0, 9)) + "fb-08d965baec1e}")
            labeling_element.appendChild(rules_element)

            rule_element = base.xml_document.createElement("rule")
            rule_element.setAttribute("key", "{feb232af-8b6c-4" + str(random.randint(10, 99)) + "c-b3e9-f27523dbd2f7}")
            rule_element.setAttribute("filter", '"SymbolID"  = ' + label_dict["labelValues"]["classId"])
            rules_element.appendChild(rule_element)
            rule_element.appendChild(settings_element)

        elif label_dict['labelValues']['type'] == 'simple':
            labeling_element.appendChild(settings_element)

        text_style_element = base.xml_document.createElement("text-style")
        for key, value in zip(
                label_dict["labelValues"]["text-style"].iterkeys(),
                label_dict["labelValues"]["text-style"].itervalues()):
            text_style_element.setAttribute(key, value)
        settings_element.appendChild(text_style_element)

        text_buffer_element = base.xml_document.createElement("text-buffer")
        for key, value in zip(label_dict["labelValues"]["text-buffer"].iterkeys(),
                              label_dict["labelValues"]["text-buffer"].itervalues()):
            text_buffer_element.setAttribute(key, value)
        text_style_element.appendChild(text_buffer_element)

        text_shadow_element = base.xml_document.createElement("shadow")
        for key, value in zip(label_dict["labelValues"]["shadow"].iterkeys(),
                              label_dict["labelValues"]["shadow"].itervalues()):
            text_shadow_element.setAttribute(key, value)
        text_style_element.appendChild(text_shadow_element)

        text_background_element = base.xml_document.createElement("background")
        for key, value in zip(label_dict["labelValues"]["background"].iterkeys(),
                              label_dict["labelValues"]["background"].itervalues()):
            text_background_element.setAttribute(key, value)
        text_style_element.appendChild(text_background_element)

        substitutions_element = base.xml_document.createElement("substitutions")
        text_style_element.appendChild(substitutions_element)

        text_format_element = base.xml_document.createElement("text-format")
        for key, value in zip(label_dict["labelValues"]["format"].iterkeys(),
                              label_dict["labelValues"]["format"].itervalues()):
            text_format_element.setAttribute(key, value)
        settings_element.appendChild(text_format_element)

        placement_element = base.xml_document.createElement("placement")
        for key, value in zip(label_dict["labelValues"]["placement"].iterkeys(),
                              label_dict["labelValues"]["placement"].itervalues()):
            placement_element.setAttribute(key, value)
        settings_element.appendChild(placement_element)

        rendering_element = base.xml_document.createElement("rendering")
        for key, value in zip(label_dict["labelValues"]["rendering"].iterkeys(),
                              label_dict["labelValues"]["rendering"].itervalues()):
            rendering_element.setAttribute(key, value)
        settings_element.appendChild(rendering_element)

        dd_properties_element = base.xml_document.createElement("dd_properties")
        settings_element.appendChild(dd_properties_element)

        option_element = base.xml_document.createElement("Option")
        option_element.setAttribute('type', 'Map')
        dd_properties_element.appendChild(option_element)

        option_child1_element = base.xml_document.createElement("Option")
        option_child1_element.setAttribute('type', 'QString')
        option_child1_element.setAttribute('name', 'name')
        option_child1_element.setAttribute('value', '')
        option_element.appendChild(option_child1_element)

        option_child2_element = base.xml_document.createElement("Option")
        option_child2_element.setAttribute('name', 'properties')
        option_element.appendChild(option_child2_element)

        option_child3_element = base.xml_document.createElement("Option")
        option_child3_element.setAttribute('type', 'QString')
        option_child3_element.setAttribute('name', 'type')
        option_child3_element.setAttribute('value', 'collection')
        option_element.appendChild(option_child3_element)
