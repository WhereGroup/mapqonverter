import re

from dictionaries.raster_stretch import stretch_dict
from modules.functions import change_interface, convert_rgb_string_to_hex
from modules.arcGisModules import ArcGisModules
from feature.fills.gradientFillSymbol import FeatureGradientFillSymbol


class RasterRenderer:
    def __init__(self):
        pass

    @staticmethod
    def create_raster_renderer_basic(base):
        """ This creates the basic raster-renderer-element in the DOM

        :param base: is the self of the renderer object containing:
            base.xml_document = xml_document
            base.map_layer_element = map_layer_element
            base.arcLayer = arc_layer
            base.layer = layer
            base.rendererType = renderer_type
        :return: pipe_element, raster_renderer_element
        """
        pipe_element = base.xml_document.createElement("pipe")
        base.map_layer_element.appendChild(pipe_element)

        raster_renderer_element = base.xml_document.createElement("rasterrenderer")
        raster_renderer_element.setAttribute("alphaBand", "-1")

        arc_raster_layer = change_interface(base.arcLayer, ArcGisModules.module_carto.IRasterLayer)
        arc_raster_effect = change_interface(arc_raster_layer, ArcGisModules.module_carto.ILayerEffects)

        try:
            opacity = str(1 - arc_raster_effect.Transparency * 0.01)
        except AttributeError:
            opacity = "1"

        raster_renderer_element.setAttribute("opacity", opacity)
        pipe_element.appendChild(raster_renderer_element)

        raster_transparency_element = base.xml_document.createElement("rasterTransparency")
        raster_renderer_element.appendChild(raster_transparency_element)

        raster_stretch = change_interface(arc_raster_layer.Renderer, ArcGisModules.module_carto.IRasterStretch2)

        if raster_stretch and raster_stretch.Background and raster_stretch.BackgroundColor.NullColor:
                values = raster_stretch.BackgroundValue
                if isinstance(values, float):
                    single_value_pixel_element = base.xml_document.createElement("singleValuePixelList")
                    raster_transparency_element.appendChild(single_value_pixel_element)
                    pixel_list_entry_element = base.xml_document.createElement("pixelListEntry")
                    single_value_pixel_element.appendChild(pixel_list_entry_element)
                    pixel_list_entry_element.setAttribute("min", unicode(int(values)))
                    pixel_list_entry_element.setAttribute("max", unicode(int(values)))
                    pixel_list_entry_element.setAttribute("percentTransparent", "100")
                else:
                    single_value_pixel_element = base.xml_document.createElement("threeValuePixelList")
                    raster_transparency_element.appendChild(single_value_pixel_element)
                    pixel_list_entry_element = base.xml_document.createElement("pixelListEntry")
                    single_value_pixel_element.appendChild(pixel_list_entry_element)
                    pixel_list_entry_element.setAttribute("red", unicode(int(values[0])))
                    pixel_list_entry_element.setAttribute("green", unicode(int(values[1])))
                    pixel_list_entry_element.setAttribute("blue", unicode(int(values[2])))
                    pixel_list_entry_element.setAttribute("percentTransparent", "100")



        min_max_origin_element = base.xml_document.createElement("minMaxOrigin")
        raster_renderer_element.appendChild(min_max_origin_element)

        origin_limits_element = base.xml_document.createElement("limits")
        origin_limits_element_content = base.xml_document.createTextNode("None")
        origin_limits_element.appendChild(origin_limits_element_content)
        min_max_origin_element.appendChild(origin_limits_element)

        origin_extent_element = base.xml_document.createElement("extent")
        origin_extent_element_content = base.xml_document.createTextNode("WholeRaster")
        origin_extent_element.appendChild(origin_extent_element_content)
        min_max_origin_element.appendChild(origin_extent_element)

        origin_stat_accuracy_element = base.xml_document.createElement("statAccuracy")
        origin_stat_accuracy_element_content = base.xml_document.createTextNode("Estimated")
        origin_stat_accuracy_element.appendChild(origin_stat_accuracy_element_content)
        min_max_origin_element.appendChild(origin_stat_accuracy_element)

        origincumulative_cut_lower_element = base.xml_document.createElement("cumulativeCutLower")
        origincumulative_cut_lower_element_content = base.xml_document.createTextNode("0.02")
        origincumulative_cut_lower_element.appendChild(origincumulative_cut_lower_element_content)
        min_max_origin_element.appendChild(origincumulative_cut_lower_element)

        origincumulative_cut_upper_element = base.xml_document.createElement("cumulativeCutUpper")
        origincumulative_cut_upper_element_content = base.xml_document.createTextNode("0.98")
        origincumulative_cut_upper_element.appendChild(origincumulative_cut_upper_element_content)
        min_max_origin_element.appendChild(origincumulative_cut_upper_element)

        originstd_dev_factor_element = base.xml_document.createElement("stdDevFactor")
        originstd_dev_factor_element_content = base.xml_document.createTextNode("2")
        originstd_dev_factor_element.appendChild(originstd_dev_factor_element_content)
        min_max_origin_element.appendChild(originstd_dev_factor_element)

        try:
            brightness_value = str(arc_raster_effect.Brightness)
            contrasts_value = str(arc_raster_effect.Contrast)

        except AttributeError:
            brightness_value = "0"
            contrasts_value = "0"

        raster_brightnesscontrast_element = base.xml_document.createElement("brightnesscontrast")
        raster_brightnesscontrast_element.setAttribute("brightness", brightness_value)
        raster_brightnesscontrast_element.setAttribute("contrast", contrasts_value)
        pipe_element.appendChild(raster_brightnesscontrast_element)

        raster_huesaturation_element = base.xml_document.createElement("huesaturation")
        raster_huesaturation_element.setAttribute("saturation ", "0")
        raster_huesaturation_element.setAttribute("grayscaleMode", "0")
        raster_huesaturation_element.setAttribute("colorizeRed", "255")
        raster_huesaturation_element.setAttribute("colorizeBlue", "128")
        raster_huesaturation_element.setAttribute("colorizeGreen", "128")
        raster_huesaturation_element.setAttribute("colorizeStrength", "100")
        raster_huesaturation_element.setAttribute("colorizeOn", "0")
        pipe_element.appendChild(raster_huesaturation_element)

        raster_resampler_element = base.xml_document.createElement("rasterresampler")
        raster_resampler_element.setAttribute("maxOversampling", "2")
        pipe_element.appendChild(raster_resampler_element)

        return pipe_element, raster_renderer_element

    @staticmethod
    def adapt_raster_renderer(base, raster_renderer_element):
        """ here the base renderer is adapted with the specific raster-renderer-content

        :param base: is the self of the renderer object containing:
            base.xml_document = xml_document
            base.map_layer_element = map_layer_element
            base.arcLayer = arc_layer
            base.layer = layer
            base.rendererType = renderer_type
        :param raster_renderer_element: the raster_renderer_element of the DOM
        """
        arc_raster_layer = change_interface(base.arcLayer, ArcGisModules.module_carto.IRasterLayer)
        renderer_name = change_interface(arc_raster_layer.Renderer, ArcGisModules.module_carto.IRasterRendererInfo).Name

        if renderer_name == "Stretched":
            if arc_raster_layer.BandCount == 3:
                RasterRenderer._create_singleband_pseudocolor_renderer(base, raster_renderer_element, arc_raster_layer)
            else:
                RasterRenderer._create_stretched_renderer(base, raster_renderer_element, arc_raster_layer)

        if renderer_name == "RGB Composite":
            RasterRenderer._create_rgb_composite_renderer(base, raster_renderer_element, arc_raster_layer)

    @staticmethod
    def _create_stretched_renderer(base, raster_renderer_element, arc_raster_layer):
        """ This creates the stretched renderer content

        :param base: is the self of the renderer object containing:
            base.xml_document = xml_document
            base.map_layer_element = map_layer_element
            base.arcLayer = arc_layer
            base.layer = layer
            base.rendererType = renderer_type
        :param raster_renderer_element: the raster_renderer_element of the DOM
        :param arc_raster_layer: ArcObject of the raster_layer
        """
        raster_renderer_element.setAttribute("type", "singlebandgray")
        raster_renderer_element.setAttribute("grayBand", "1")

        renderer = change_interface(
            arc_raster_layer.Renderer,
            ArcGisModules.module_carto.IRasterStretchColorRampRenderer
        )

        sbg_high = renderer.LabelHigh[7:].split(',')[0]
        sbg_min = renderer.LabelLow[6:].split(',')[0]
        sbg_gradient = re.sub(r'[\s+]', '', renderer.ColorScheme.title())
        raster_renderer_element.setAttribute("gradient", sbg_gradient)

        raster_contrast_enhancement_element = base.xml_document.createElement("contrastEnhancement")
        raster_renderer_element.appendChild(raster_contrast_enhancement_element)

        sbg_min_value_element = base.xml_document.createElement("minValue")
        sbg_min_value_element_content = base.xml_document.createTextNode(sbg_min)
        sbg_min_value_element.appendChild(sbg_min_value_element_content)
        raster_contrast_enhancement_element.appendChild(sbg_min_value_element)

        sbg_max_value_element = base.xml_document.createElement("maxValue")
        sbg_max_value_element_content = base.xml_document.createTextNode(sbg_high)
        sbg_max_value_element.appendChild(sbg_max_value_element_content)
        raster_contrast_enhancement_element.appendChild(sbg_max_value_element)

        sbg_algorithm_element = base.xml_document.createElement("algorithm")
        sbg_algorithm_element_content = base.xml_document.createTextNode("StretchToMinimumMaximum")
        sbg_algorithm_element.appendChild(sbg_algorithm_element_content)
        raster_contrast_enhancement_element.appendChild(sbg_algorithm_element)

    @staticmethod
    def _create_rgb_composite_renderer(base, raster_renderer_element, arc_raster_layer):
        """ This creates the rgb-composite renderer content

        :param base: is the self of the renderer object containing:
            base.xml_document = xml_document
            base.map_layer_element = map_layer_element
            base.arcLayer = arc_layer
            base.layer = layer
            base.rendererType = renderer_type
        :param raster_renderer_element: the raster_renderer_element of the DOM
        :param arc_raster_layer: ArcObject of the raster_layer
        """
        raster_renderer_element.setAttribute("type", "multibandcolor")
        raster_renderer_element.setAttribute("redBand", "1")
        raster_renderer_element.setAttribute("greenBand", "2")
        raster_renderer_element.setAttribute("blueBand", "3")

        raster_stretch = change_interface(arc_raster_layer.Renderer, ArcGisModules.module_carto.IRasterStretch2)

        limits_element = raster_renderer_element.getElementsByTagName('limits')[0]
        limits_element.firstChild.nodeValue = stretch_dict.get(raster_stretch.StretchType, 'None')

        stretch_params = raster_stretch.StandardDeviationsParam
        raster_renderer_element.getElementsByTagName('stdDevFactor')[0].firstChild.nodeValue = unicode(stretch_params)

        no_data_element = base.xml_document.createElement("noData")
        for band_index in range(1, 4):
            no_data_list_element = base.xml_document.createElement("noDataList")
            no_data_list_element.setAttribute("bandNo", unicode(band_index))
            no_data_list_element.setAttribute("useSrcNoData", "0")

            no_data_range_element = base.xml_document.createElement("noDataRange")
            no_data_range_element.setAttribute("min", "0")
            no_data_range_element.setAttribute("max", "0")

            no_data_list_element.appendChild(no_data_range_element)
            no_data_element.appendChild(no_data_list_element)

        base.map_layer_element.appendChild(no_data_element)

        if not raster_stretch.StretchType == 0:
            bandstats = RasterRenderer._get_band_stats(arc_raster_layer.Raster)

            color = ["placeholder", "red", "green", "blue"]

            for x in range(1, 4):
                raster_contrast_enhancement_element = base.xml_document.createElement(color[x] + "ContrastEnhancement")
                raster_renderer_element.appendChild(raster_contrast_enhancement_element)

                renderer_contrast_min_element = base.xml_document.createElement("minValue")
                renderer_contrast_min_element_content = base.xml_document.createTextNode(
                    bandstats.get(x, {}).get("min")
                )
                renderer_contrast_min_element.appendChild(renderer_contrast_min_element_content)
                raster_contrast_enhancement_element.appendChild(renderer_contrast_min_element)

                renderer_contrast_max_element = base.xml_document.createElement("maxValue")
                renderer_contrast_max_element_content = base.xml_document.createTextNode(
                    bandstats.get(x, {}).get("max")
                )
                renderer_contrast_max_element.appendChild(renderer_contrast_max_element_content)
                raster_contrast_enhancement_element.appendChild(renderer_contrast_max_element)

                renderer_contrast_algorithm_element = base.xml_document.createElement("algorithm")
                renderer_contrast_algorithm_element_content = base.xml_document.createTextNode(
                    'StretchToMinimumMaximum'
                )
                renderer_contrast_algorithm_element.appendChild(renderer_contrast_algorithm_element_content)
                raster_contrast_enhancement_element.appendChild(renderer_contrast_algorithm_element)

    @staticmethod
    def _create_singleband_pseudocolor_renderer(base, raster_renderer_element, arc_raster_layer):
        renderer = change_interface(
            arc_raster_layer.Renderer,
            ArcGisModules.module_carto.IRasterStretchColorRampRenderer
        )

        color_ramp_properties = FeatureGradientFillSymbol.create_color_ramp_properties(
            renderer.ColorRamp,
            False,
            {'dict_symbols': {}}
        )

        bandstats = RasterRenderer._get_band_stats(arc_raster_layer.Raster)
        used_band_number = renderer.BandIndex + 1

        raster_renderer_element.setAttribute("type", "singlebandpseudocolor")
        raster_renderer_element.setAttribute("band", unicode(used_band_number))
        raster_renderer_element.setAttribute("alphaBand", unicode(used_band_number))
        raster_renderer_element.setAttribute("classificationMin", bandstats.get(used_band_number, {}).get("min"))
        raster_renderer_element.setAttribute("classificationMax", bandstats.get(used_band_number, {}).get("max"))

        rastershader_element = base.xml_document.createElement("rastershader")
        raster_renderer_element.appendChild(rastershader_element)

        colorrampshader_element = base.xml_document.createElement("colorrampshader")
        colorrampshader_element.setAttribute("maximumValue", renderer.LabelHigh)
        colorrampshader_element.setAttribute("minimumValue", renderer.LabelLow)
        colorrampshader_element.setAttribute("classificationMode", "2")
        colorrampshader_element.setAttribute("clip", "0")
        colorrampshader_element.setAttribute("colorRampType", "INTERPOLATED")
        rastershader_element.appendChild(colorrampshader_element)

        colorramp_element = base.xml_document.createElement("colorramp")
        colorramp_element.setAttribute("name", "[source]")
        colorramp_element.setAttribute("type", "gradient")

        color1_prop = base.xml_document.createElement("prop")
        color1_prop.setAttribute("k", "color1")
        color1_prop.setAttribute("v", color_ramp_properties["dict_symbols"]["color1"])
        color2_prop = base.xml_document.createElement("prop")
        color2_prop.setAttribute("k", "color2")
        color2_prop.setAttribute("v", color_ramp_properties["dict_symbols"]["color2"])
        stops_prop = base.xml_document.createElement("prop")
        stops_prop.setAttribute("k", "stops")
        stops_prop.setAttribute("v", color_ramp_properties["dict_symbols"]["stops"])
        discrete_prop = base.xml_document.createElement("prop")
        discrete_prop.setAttribute("k", "discrete")
        discrete_prop.setAttribute("v", "0")
        ramp_type_prop = base.xml_document.createElement("prop")
        ramp_type_prop.setAttribute("k", "rampType")
        ramp_type_prop.setAttribute("v", "gradient")

        colorramp_element.appendChild(color1_prop)
        colorramp_element.appendChild(color2_prop)
        colorramp_element.appendChild(stops_prop)
        colorramp_element.appendChild(discrete_prop)
        colorramp_element.appendChild(ramp_type_prop)

        colorrampshader_element.appendChild(colorramp_element)

        color_stops = color_ramp_properties["dict_symbols"]["stops"].split(":")
        for index, color in enumerate(color_stops[:-1]):
            position_double, color_value = color.split(";")
            item_element = base.xml_document.createElement("item")
            color_value_hex = convert_rgb_string_to_hex(color_value)
            item_element.setAttribute("color", color_value_hex)
            item_element.setAttribute("alpha", color_value[-3:])
            value = unicode(255*float(position_double)) if index < len(color_stops) else u"255"
            item_element.setAttribute("value", value)
            item_element.setAttribute("label", value)
            colorrampshader_element.appendChild(item_element)

    @staticmethod
    def _get_band_stats(arc_raster):
        arc_raster = change_interface(arc_raster, ArcGisModules.module_data_source_raster.IRaster2)
        arc_raster_dataset = change_interface(arc_raster.RasterDataset, ArcGisModules.module_gdb.IRasterDataset)
        arc_raster_band_collection = change_interface(
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
                band_minimum = 0
                band_maximum = 255

            bandstats.update(
                {x:
                    {
                        "min": unicode(int(band_minimum)),
                        "max": unicode(int(band_maximum)),
                    }
                }
            )

        return bandstats
