import arcpy

from feature.featureRenderer import FeatureRenderer
from labelRenderer import LabelRenderer
from nullRenderer import NullRenderer
from rasterRenderer import RasterRenderer
from wmsRenderer import WMSRenderer


class Renderer:

    def __init__(self, document, map_layer_element, arc_layer, layer, renderer_type):
        self.document = document
        self.map_layer_element = map_layer_element
        self.arcLayer = arc_layer
        self.layer = layer
        self.rendererType = renderer_type

    def get_renderer(self):
        """ Depending on type the maplayer-element gets specific renderer-node"""
        if self.rendererType == "raster":
            pipe, raster_renderer_element = RasterRenderer.create_raster_renderer_basic(self)
            self.map_layer_element.appendChild(pipe)
            RasterRenderer.adapt_raster_renderer(self, raster_renderer_element)

        elif self.rendererType == "feature":
            feature_renderer = FeatureRenderer()
            feature_renderer.create_feature_renderer(self)

        elif self.rendererType == "wms":
            pipe, raster_renderer_element = RasterRenderer.create_raster_renderer_basic(self)
            self.map_layer_element.appendChild(pipe)
            WMSRenderer.adapt_wms_renderer(raster_renderer_element)

        elif self.rendererType == "gdb":
            NullRenderer.create_null_symbol_renderer(self)
            LabelRenderer.create_labels(self, self.map_layer_element,
                                        label_dict=LabelRenderer.get_label_dict(
                                                base=self,
                                                renderer_type=self.rendererType
                                                )
                                        )
            arcpy.AddWarning(
                "\t\tLabels have been converted. Complex Labeling is not supported. Check QGIS-File for result!"
            )
        else:
            print "unknown type"
