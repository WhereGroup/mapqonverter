# MapQonverter
The MapQonverter converts an ArcMap Project to a QGIS Project.
The script is inspired by Mxd2Qgs from Allan Maungu.

System Requirements: at least ArcMap 10.4. While ArcMap 10.7 is fully tested

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
  * Character-Marker
* Lines
  * Hash-Lines
  * Marker-Lines
  * Simple-Lines
  * Cartographic-Lines
* Fills
  * Gradient-Fill
    * RadialFill is not yet supported.
  * Line-Fill
  * Marker-Fill
  * Random-Fill
  * Simple-Fill
  * Outlines -> QGIS Rand (Simple, Marker, Hashed)  
* Multi-Layer-Symbols
* Unique-Values
* Graduated-Colors / Graduated–Symbols
	
#### WMS-Layer

#### GeoDataBase-Annotation – Layer

#### Database-Layer
  * Just Postgresql is fully tested

#### Labels
  * Simple Labels are supported, for example city-/country-names. Complex logical expressions are hardly translatable from VBScript (ArcMap) zur QGIS Expressions Engine. 

#### Layout
* The Layout will be safed as "Imported Layout"
    * Basic NorthArrow will be exported
    * Legend 
    * Polygone, Ellipses, Line-, and PolyLine-Elements
    * ScaleBars 
    * TextElements
    * Pictures

#### Logging
* A Logfile is generated after the Export in the Folder "logs"

### Packages
[comtypes](https://pypi.org/project/comtypes/)
