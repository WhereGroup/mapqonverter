from modules.arcGisModules import ArcGisModules
from modules.functions import type_cast_module


class GraduatedColorsRenderer:
    def __init__(self):
        pass

    @staticmethod
    def create_graduated_colors_element(base, renderer, symbols):
        """This creates the graduated-colors-renderer-element in the DOM

        :param base: is the self of the renderer object
        :param renderer: is the renderer-element in the DOM
        :param symbols: is the list of used symbols of the renderer
        """
        renderer.setAttribute("type", "graduatedSymbol")
        renderer.setAttribute("symbollevels", "0")
        renderer.setAttribute("graduatedMethod", "GraduatedColor")
        renderer.setAttribute("attr", base.layer.symbology.valueField)

        graduated_layer = type_cast_module(base.arcLayer, ArcGisModules.module_carto.IGeoFeatureLayer)
        graduated_renderer = type_cast_module(graduated_layer.Renderer, ArcGisModules.module_carto.IClassBreaksRenderer)

        for each in range(0, base.layer.symbology.numClasses):
            symbols.append(graduated_renderer.Symbol[each])

        # Create ranges Element
        ranges_element = base.document.createElement("ranges")
        renderer.appendChild(ranges_element)

        # Create each range element
        for index, (label, value) in enumerate(
                zip(base.layer.symbology.classBreakLabels, base.layer.symbology.classBreakValues)):
            range_element = base.document.createElement("range")
            range_element.setAttribute("render", "true")
            range_element.setAttribute("symbol", str(index))
            range_element.setAttribute("label", label)
            range_element.setAttribute("lower", str(value))
            range_element.setAttribute("upper", str(base.layer.symbology.classBreakValues[index + 1]))
            ranges_element.appendChild(range_element)
