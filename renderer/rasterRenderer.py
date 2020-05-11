import re

from modules.snippets102 import type_cast_module
from modules.arcGisModules import ArcGisModules


class RasterRenderer:
    def __init__(self):
        pass

    @staticmethod
    def create_raster_renderer_basic(base):
        """ This creates the basic raster-renderer-element in the DOM

        :param base: is the self of the renderer object
        :return: pipe_element, raster_renderer_element
        """
        pipe_element = base.document.createElement("pipe")
        base.map_layer_element.appendChild(pipe_element)

        raster_renderer_element = base.document.createElement("rasterrenderer")
        raster_renderer_element.setAttribute("alphaBand", "-1")

        arc_raster_layer = type_cast_module(base.arcLayer, ArcGisModules.module_carto.IRasterLayer)
        arc_raster_effect = type_cast_module(arc_raster_layer, ArcGisModules.module_carto.ILayerEffects)

        try:
            opacity = str(1 - arc_raster_effect.Transparency * 0.01)
        except AttributeError:
            opacity = "1"

        raster_renderer_element.setAttribute("opacity", opacity)
        pipe_element.appendChild(raster_renderer_element)

        raster_transparency_element = base.document.createElement("rasterTransparency")
        raster_renderer_element.appendChild(raster_transparency_element)

        min_max_origin_element = base.document.createElement("minMaxOrigin")
        raster_renderer_element.appendChild(min_max_origin_element)

        origin_limits_element = base.document.createElement("limits")
        origin_limits_element_content = base.document.createTextNode("CumulativeCut")
        origin_limits_element.appendChild(origin_limits_element_content)
        min_max_origin_element.appendChild(origin_limits_element)

        origin_extent_element = base.document.createElement("extent")
        origin_extent_element_content = base.document.createTextNode("WholeRaster")
        origin_extent_element.appendChild(origin_extent_element_content)
        min_max_origin_element.appendChild(origin_extent_element)

        origin_stat_accuracy_element = base.document.createElement("statAccuracy")
        origin_stat_accuracy_element_content = base.document.createTextNode("Estimated")
        origin_stat_accuracy_element.appendChild(origin_stat_accuracy_element_content)
        min_max_origin_element.appendChild(origin_stat_accuracy_element)

        origincumulative_cut_lower_element = base.document.createElement("cumulativeCutLower")
        origincumulative_cut_lower_element_content = base.document.createTextNode("0.005")
        origincumulative_cut_lower_element.appendChild(origincumulative_cut_lower_element_content)
        min_max_origin_element.appendChild(origincumulative_cut_lower_element)

        origincumulative_cut_upper_element = base.document.createElement("cumulativeCutUpper")
        origincumulative_cut_upper_element_content = base.document.createTextNode("0.995")
        origincumulative_cut_upper_element.appendChild(origincumulative_cut_upper_element_content)
        min_max_origin_element.appendChild(origincumulative_cut_upper_element)

        originstd_dev_factor_element = base.document.createElement("stdDevFactor")
        originstd_dev_factor_element_content = base.document.createTextNode("2")
        originstd_dev_factor_element.appendChild(originstd_dev_factor_element_content)
        min_max_origin_element.appendChild(originstd_dev_factor_element)

        try:
            brightness_value = str(arc_raster_effect.Brightness)
            contrasts_value = str(arc_raster_effect.Contrast)

        except AttributeError:
            brightness_value = "0"
            contrasts_value = "0"

        raster_brightnesscontrast_element = base.document.createElement("brightnesscontrast")
        raster_brightnesscontrast_element.setAttribute("brightness", brightness_value)
        raster_brightnesscontrast_element.setAttribute("contrast", contrasts_value)
        pipe_element.appendChild(raster_brightnesscontrast_element)

        raster_huesaturation_element = base.document.createElement("huesaturation")
        raster_huesaturation_element.setAttribute("saturation ", "0")
        raster_huesaturation_element.setAttribute("grayscaleMode", "0")
        raster_huesaturation_element.setAttribute("colorizeRed", "255")
        raster_huesaturation_element.setAttribute("colorizeBlue", "128")
        raster_huesaturation_element.setAttribute("colorizeGreen", "128")
        raster_huesaturation_element.setAttribute("colorizeStrength", "100")
        raster_huesaturation_element.setAttribute("colorizeOn", "0")
        pipe_element.appendChild(raster_huesaturation_element)

        raster_resampler_element = base.document.createElement("rasterresampler")
        raster_resampler_element.setAttribute("maxOversampling", "2")
        pipe_element.appendChild(raster_resampler_element)

        return pipe_element, raster_renderer_element

    @staticmethod
    def adapt_raster_renderer(base, raster_renderer_element):
        """ here the base renderer is adapted with the specific raster-renderer-content

        :param base: is the self of the renderer object
        :param raster_renderer_element: the raster_renderer_element of the DOM
        """
        arc_raster_layer = type_cast_module(base.arcLayer, ArcGisModules.module_carto.IRasterLayer)
        renderer_name = type_cast_module(arc_raster_layer.Renderer, ArcGisModules.module_carto.IRasterRendererInfo).Name

        if arc_raster_layer.BandCount == 1 and renderer_name == "Stretched":
            RasterRenderer._create_stretched_renderer(base, raster_renderer_element, arc_raster_layer)

        if arc_raster_layer.BandCount == 3 and renderer_name == "RGB Composite":
            RasterRenderer._create_rgb_composite_renderer(base, raster_renderer_element, arc_raster_layer)

    @staticmethod
    def _create_stretched_renderer(base, raster_renderer_element, arc_raster_layer):
        """ This creates the stretched renderer content

        :param base: is the self of the renderer object
        :param raster_renderer_element: the raster_renderer_element of the DOM
        :param arc_raster_layer: ArcObject of the raster_layer
        """
        raster_renderer_element.setAttribute("type", "singlebandgray")
        raster_renderer_element.setAttribute("grayBand", "1")

        renderer = type_cast_module(
            arc_raster_layer.Renderer,
            ArcGisModules.module_carto.IRasterStretchColorRampRenderer
        )

        sbg_high = renderer.LabelHigh[7:].split(',')[0]
        sbg_min = renderer.LabelLow[6:].split(',')[0]
        sbg_gradient = re.sub(r'[\s+]', '', renderer.ColorScheme.title())
        raster_renderer_element.setAttribute("gradient", sbg_gradient)

        raster_contrast_enhancement_element = base.document.createElement("contrastEnhancement")
        raster_renderer_element.appendChild(raster_contrast_enhancement_element)

        sbg_min_value_element = base.document.createElement("minValue")
        sbg_min_value_element_content = base.document.createTextNode(sbg_min)
        sbg_min_value_element.appendChild(sbg_min_value_element_content)
        raster_contrast_enhancement_element.appendChild(sbg_min_value_element)

        sbg_max_value_element = base.document.createElement("maxValue")
        sbg_max_value_element_content = base.document.createTextNode(sbg_high)
        sbg_max_value_element.appendChild(sbg_max_value_element_content)
        raster_contrast_enhancement_element.appendChild(sbg_max_value_element)

        sbg_algorithm_element = base.document.createElement("algorithm")
        sbg_algorithm_element_content = base.document.createTextNode("StretchToMinimumMaximum")
        sbg_algorithm_element.appendChild(sbg_algorithm_element_content)
        raster_contrast_enhancement_element.appendChild(sbg_algorithm_element)

    @staticmethod
    def _create_rgb_composite_renderer(base, raster_renderer_element, arc_raster_layer):
        """ This creates the rgb-composite renderer content

        :param base: is the self of the renderer object
        :param raster_renderer_element: the raster_renderer_element of the DOM
        :param arc_raster_layer: ArcObject of the raster_layer
        """
        raster_renderer_element.setAttribute("type", "multibandcolor")
        raster_renderer_element.setAttribute("redBand", "1")
        raster_renderer_element.setAttribute("greenBand", "2")
        raster_renderer_element.setAttribute("blueBand", "3")

        # find the statistics for the 3 bands
        arc_raster = arc_raster_layer.Raster
        arc_raster = type_cast_module(arc_raster, ArcGisModules.module_data_source_raster.IRaster2)
        arc_raster_dataset = arc_raster.RasterDataset
        arc_raster_dataset = type_cast_module(arc_raster_dataset, ArcGisModules.module_gdb.IRasterDataset)
        arc_raster_band_collection = type_cast_module(
            arc_raster_dataset,
            ArcGisModules.module_data_source_raster.IRasterBandCollection
        )

        bandstats = {}

        for x in range(1, arc_raster_band_collection.Count + 1):
            raster_band = arc_raster_band_collection.BandByName("Band_" + str(x))
            try:
                band_minimum = raster_band.Statistics.Minimum
                band_maximum = raster_band.Statistics.Maximum
            except ValueError:
                # arcpy.AddWarning(
                #    "\t\tProblem occured while reading out Band-Stats from Rasterlayer." +
                #    "Default Values are min = 0, max = 255. \n\t\t(If you don't know what this means, " +
                #    "there is probably no problem."
                # ) -> Log instead
                band_minimum = 0
                band_maximum = 255

            bandstats.update(
                {x:
                    {
                        "min": str(int(band_minimum)),
                        "max": str(int(band_maximum)),
                    }
                 }
            )

        # create the dom elements
        color = ["placeholder", "red", "green", "blue"]
        for x in range(1, 4):
            raster_contrast_enhancement_element = base.document.createElement(color[x] + "ContrastEnhancement")
            raster_renderer_element.appendChild(raster_contrast_enhancement_element)

            renderer_contrast_min_element = base.document.createElement("minValue")
            renderer_contrast_min_element_content = base.document.createTextNode(
                bandstats.get(x, {}).get("min")
            )
            renderer_contrast_min_element.appendChild(renderer_contrast_min_element_content)
            raster_contrast_enhancement_element.appendChild(renderer_contrast_min_element)

            renderer_contrast_max_element = base.document.createElement("maxValue")
            renderer_contrast_max_element_content = base.document.createTextNode(
                bandstats.get(x, {}).get("max")
            )
            renderer_contrast_max_element.appendChild(renderer_contrast_max_element_content)
            raster_contrast_enhancement_element.appendChild(renderer_contrast_max_element)

            renderer_contrast_algorithm_element = base.document.createElement("algorithm")
            renderer_contrast_algorithm_element_content = base.document.createTextNode(
                "StretchToMinimumMaximum"
            )
            renderer_contrast_algorithm_element.appendChild(renderer_contrast_algorithm_element_content)
            raster_contrast_enhancement_element.appendChild(renderer_contrast_algorithm_element)
