from modules.arcGisModules import ArcGisModules
from modules.snippets102 import type_cast_module


class UniqueValueRenderer:
    def __init__(self):
        pass

    @staticmethod
    def create_unique_values_element(base, renderer, symbols):
        """This creates the unique-value-renderer-element in the DOM

        :param base: is the self of the renderer object
        :param renderer: is the renderer-element in the DOM
        :param symbols: is the list of used symbols of the renderer
        """
        renderer.setAttribute("type", "categorizedSymbol")
        renderer.setAttribute("attr", base.layer.symbology.valueField)

        unique_layer = type_cast_module(base.arcLayer, ArcGisModules.module_carto.IGeoFeatureLayer)
        unique_renderer = type_cast_module(unique_layer.Renderer, ArcGisModules.module_carto.IUniqueValueRenderer)

        # Create Pointer on Symbols for each UniqueValue
        for each in base.layer.symbology.classLabels:
            symbols.append(unique_renderer.Symbol[each])

        # Create categories Element
        categories_element = base.document.createElement("categories")
        renderer.appendChild(categories_element)

        labels = base.layer.symbology.classLabels
        label_values = base.layer.symbology.classValues
        # Create each category element
        for index, (label, value) in enumerate(zip(labels, label_values)):
            category_element = base.document.createElement("category")
            category_element.setAttribute("render", "true")
            category_element.setAttribute("symbol", str(index))
            category_element.setAttribute("label", label)
            category_element.setAttribute("value", value)
            categories_element.appendChild(category_element)
