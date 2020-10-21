from modules.arcGisModules import ArcGisModules
from modules.functions import change_interface


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
        geo_feature_layer = change_interface(base.arcLayer, ArcGisModules.module_carto.IGeoFeatureLayer)
        unique_renderer = change_interface(geo_feature_layer.Renderer, ArcGisModules.module_carto.IUniqueValueRenderer)

        renderer.setAttribute("type", "categorizedSymbol")
        renderer.setAttribute("attr", unique_renderer.Field[0])

        categories_element = base.xml_document.createElement("categories")
        renderer.appendChild(categories_element)

        last_index = unique_renderer.ValueCount
        for index in range(0, last_index + 1):
            value = "" if index == last_index else unique_renderer.Value[index]

            symbols.append(
                unique_renderer.DefaultSymbol if index == last_index else unique_renderer.Symbol[value]
            )

            category_element = base.xml_document.createElement("category")
            category_element.setAttribute("render", "true")
            category_element.setAttribute("symbol", str(index))
            category_element.setAttribute("value", value)
            category_element.setAttribute("label",
                                          unique_renderer.DefaultLabel if index == last_index
                                          else unique_renderer.Label[value]
                                          )
            categories_element.appendChild(category_element)
