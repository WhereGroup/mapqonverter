# Mapqonverter
The Mapqonverter converts an ArcMap Project to a QGIS Project

## Installation

```bash
# Clone repository
git clone https://github.com/WhereGroup/mapqonverter.git

# Download Python package comtypes
pip install comtypes

```
> :warning: If you have more than one python version on your pc, be sure to install comtypes to the python version used by ArcMap - for example: C:\Python27\ArcGIS10.7

- Add toolbox "Mapqonverter.tbx" to ArcMap 
- Start script "ArcMap Project to QGIS project"
- Choose filename and directory for QGIS-File
- Export
- Smile

> :rewind: If you do not work with ArcMap 10.7, you can change /modules/snippets102.py line 36 to your used version

## Functionality
The following can be converted:

#### Legend

The legend, including Grouplayer and nested structures.

* Because the structure is build from the LongName, two layers can't have the same name and be direct neighbours, sad. 

#### DataFrames 

* Dataframes will be exported as Grouplayers.

#### Rasterlayer

* Stretched
* RGB Composite
* Color-Map

#### Featurelayer

* Marker
  * Simple-Marker
    * EsriMarker/CharacterMarker are not yet supported.
* Lines
  * Hash-Lines
  * Marker-Lines
  * Simple-Lines
  * Cartographic-Lines
  * Simple-Lines
* Fills
  * Gradient-Fill
    * RadialFill is not yet supported.
  * Line-Fill
  * Marker-Fill
    * Random-Fill is not yet supported.
  * Simple-Fill
  * Outlines -> QGIS Rand (Simple, Marker, Hashed)  
* Multi-Layer-Symbols
* Unique-Values
* Graduated-Colors / Graduated–Symbols
	
#### WMS-Layer

* just tested with raster-based WMS.

#### GeoDataBase-Annotation – Layer
  * Just Annotations - GeoDataBase-Geometries are not yet supported.

#### Database-Layer
  * Just Postgresql is fully tested

#### Labels
  * Simple Labels are supported, for example city-/country-names. Complex logical expressions are hardly translatable from VBScript (ArcMap) zur QGIS Expressions Engine. 

## Packages
[comtypes](https://pypi.org/project/comtypes/)
