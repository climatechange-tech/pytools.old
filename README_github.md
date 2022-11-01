# ESPON-Climate Update 2022
***
This repository contains modules that were used in the generation of the exposure 
and hazard database used in the risk analysis of ESPON-Climate Update 2022.

The module called **project_parameters.py** controls all the processes of the rest
of the modules. The idea of this module is to grouped all the dynamic parameters 
of the project. In that way when any of the code of this project is used in
another project we can change only this module. However, this is an ongoing process.
In REACHOUT the main role of this module has been improved.

# Pre-processing modules
This are modules that can be applied at the beginning of the process:

* **create_reference_images.py**: using the 50 m LUISA grid this module creates a reference
  images for some outer territories. Since the ESPON area includes all the outer territories,
some of them has to be processed separately to avoid including large territories of sea that 
  we do not need to process. This outer territories are Guadoulupe, Martinique, Guyane,
  Mayotte and Reunion. The result are 5 tif files (Guadoulupe and Martinique share
  the same grid and Europe).

* **download_agroclimatic_indicators.py**: This module downloads the
agroclimatic indicators database used to characterise the climate related hazards 
  (https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-agroclimatic-indicators?tab=overview).

* **download_fire_danger_indicators.py**:This module downloads the
fire danger indicators database used to characterise the hazard related to fire 
  (https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-tourism-fire-danger-indicators?tab=overview)

* **rasterise_shapefile.py**: Is a generic module to rasterise a given shapefile
based on a reference raster image. It was designed to rasterise those assets provided
  in shapefile format. The reference images are those created by 
  **create_reference_images.py**.

* **resampling_raster**: this module just calls the generic tool of general_functions called 
resample_raster (**raster_tools.py**). It is used to downscale PESETA IV data to
  LUISA 50m reference grid.

* **processing_mask_cordex.py**: this module generates a binary mask. The ones
represent the areas with CORDEX data, while the zeros are areas without CORDEX data.
  This is due to the fact that CORDEX is processed in curved reference system, so 
  when it is reprojected to, for example, WGS84 we can see how its area acquires
  a curved shape. In that way this mask is used in posterior processings to filter
  out the areas with no data.

# Hazard database
To create the hazard database we considered three main topics whose information
comes from three main input datasets. All the indicators related to the generic 
hazards of the climate (temperature, frost days, etc) were taken from the agroclimatic 
indicators database of the Copernicus Climate Data Store (CDS). The days with fire
danger were provided by the fire danger indicators database of the CDS. Finally,
we characterised the floods with the last outputs of the PESETA IV project.

In all the indicators coming from the agroclimatic indicators the processing was the same.
First an annual metric is computed (sum, mean or max). Then we applied a multi-year 
average and multi-model average. Finally, we averaged spatially per NUTS3:

* **hazard_consecutive_dry_days**
* **hazard_frost_days**
* **hazard_mean_precipitation**
* **hazard_mean_temperature**
* **hazard_summer_days**
* **hazard_tropical_nights**
* **hazard_very_heavy_rainfall**

In the case of the fire danger indicators, in a first step we regularised the 
dataset with CDO since the database comes in a curved reference system 
(**preprocessing_hazard_fire_danger.py**). Then we applied a multi-year average.
it is not necessary to apply a multi-model average since the ensemble result can 
be downloaded directly. Finally we apply a spatial average per NUTS3 
(**hazard_fire_danger_days.py**).

In both agroclimatic indicators and fire danger indicators the step of applying the 
spatial average is performed by the module **hazard_from_global_to_nuts3.py**.

In the case of the coastal flooding we computed the change in frequency of the 
100-year event to the future comparing future and historical extreme sea levels.
In a first step, we transformed the original netCDF to a point shapefile
(**preprocessing_hazard_esl.py**). In this shapefile the columns are flood 
depths of several return periods. In a second step we compute the future 
return period by interpolation (**hazard_coastal_floods.py**).

In the case of the river floods the change in frequency is already provided by
PESETA IV. However, the netCDF that can be downloaded from their webpage is not 
correctly structured or at least when opening with gdal the image is transposed.
So **preprocessing_hazard_river_runoff.py** is used to correctly save the image.
Then, **hazard_riverine_floods** computes the spatial average of the future return 
period per NUTS3 region. The spatial average is weighted by the proportion of flooded
area.  

# Exposure database
The exposure database aims to determine the amount of a given asset that is exposed to
a given hazard. A module has been generated per each of the assets. However, in general terms,
we applied two procedures depending on the hazards. On the one hand, when the hazard is
continuous in space we used the total amount of the asset in the region. On the other hand,
if the hazard is discrete in space (e.g. flooded area) the exposure is the amount of 
assets that fall within the hazardous area. In most cases, for consistency, we took
the exposure from the Risk Data Hub (RDH) directly, so we inherited the units.

We generate two versions. The main change was that in the first version we generated indicators 
based on our own analysis, while in the second version we took the information from RDH directly.

* **exposure_agriculture_forestry.py** (km<sup>2</sup>): 
  * Version 1.0: from LUISA base map. Agriculture codes: 2110, 2120, 2130, 2210, 2220, 2230, 2310, 
    2410, 2420, 2430, 2440. Forestry codes: 2440, 3110, 3120, 3130.
  * Version 1.1: from RDH.
* **exposure_airports.py** (count): number of airports coming from EUROSTAT GISCO
* **exposure_education_facilities.py** (million EUR): 
  * Version 1.1: from RDH
* **exposure_harbours.py** (count): number of harbours coming from EUROSTAT GISCO
* **exposure_industrial.py** (km<sup>2</sup>):
  * Version 1.0: from LUISA base map. Codes: 1210.
  * Version 1.1: from RDH.
* **exposure_museums.py** (count):
  * Version 1.0: from OpenStreetMap. Number of museums.
  * Version 1.1: from Cultural Gems. Number of museums.
* **exposure_population.py** (persons):
  * Version 1.0: the total from EUROSTAT and the spatially explicit information from 
    GEOSTAT 2018 at 1 km.
  * Version 1.1: from RDH.
* **exposure_protected_areas.py** (km<sup>2</sup>):
  * Version 1.0: from EEA Protected areas.
  * Version 1.1: from RDH.
* **exposure_railway_stations.py** (count): number of airports coming from
  OpenStreetMap
* **exposure_railways.py** (k tonnes):
  * Version 1.0: from OpenStreetMap (length km).
  * Version 1.1: from RDH.
* **exposure_refineries.py** (count): number of airports coming from 
  EEA E-PRTR
* **exposure_roads.py** (k tonnes):
  * Version 1.0: from OpenStreetMap (length km).
  * Version 1.1: from RDH.
* **exposure_settlements.py** (km<sup>2</sup>):
  * Version 1.0: from LUISA base map. Codes: 1111, 1121, 1122, 1123.
  * Version 1.1: from RDH.
* **exposure_thermal_power_plants.py** (count): number of thermal power plants
  coming from EEA E-PRTR
* **exposure_world_heritage_sites.py** (count): number of WHS coming from 
  UNESCO
  
- **exposure_from_rdh.py**: general exposure functions to take data from RDH used by
the previous codes that are based in RDH.
  
Excluded:
* **exposure_energy.py**: initially the idea was to include the GVA and the employment
  in the service sector. Finally, we excluded the energy sector since this data 
  is not spatially explicit (comes from EUROSTAT). 
* **exposure_tourism.py**: the idea was to include the number of establishments. 
  Finally, we excluded the energy sector since this data is not spatially explicit
  (comes from EUROSTAT). 
  
# Post-processing modules
These modules aim to apply the last formatting to the hazard and exposure database:

* **postprocessing_format_unique_gpkg.py**: creates a uniqe gpkg with a given layer
  structure: historical exposure, historical hazard, rcp2.6 hazard, rcp4.5 
  hazard and rcp8.5 hazard.
* **postprocessing_set_missing_values.py**: set the correct missing values on each
indicator based on the coverage of the input dataset and other assumptions done
  within the project. It is applied to the unique gpkg.
* **postprocessing_combine_versions.py**: since ESPON-Climate was an evolving project
we developed several versions of the hazard and exposure database. This module combines 
  two version keeping those indicators that have not changed and inserting the updated
  indicators.

# Exploratory modules
These are modules that are not part of the process. They have a exploratory 
or testing objective:

* **postprocessing_get_distribution_metrics.py**: in order to correctly normalise 
  the indicators between 1 (very low hazard) and 2 (very high hazard) it was necessary to 
  see their distribution. This module generates histogram plots.
* **postprocessing_check_rdh_quality.py**: This module's objective is to analyse
  if the sum of the components of the exposure provided by RDH 
  correspond to the total provided by RDH. It is a quality checking.
* **hazard_riverine_floods_proportion.py**: extracts the flooded proportion per
5 km x 5 km grid cell of PESETA river runoff dataset. The resulting image was
  used to generate a figure for the report.

Besides, we initially used the following modules to analyse and explore the Aqueduct
dataset that was not  finally used in the hazard database:

* **create_aggregated_flood_maps.py**: Aqueduct provides maps for several return periods at global scale.
This module creates accumulated maps of the return periods for each model and year. The result
is a raster were each pixel is identified with the return period were the flood depth was 
  above 0.
  
* **create_common_flood_maps.py**: Aqueduct provides maps for several return periods at global scale.
This module generates raster maps were each pixel determines the agreement between models.
  For example, if a pixel has a value of 5 means that 5 models have agreed that this pixel
  will be flooded (flood depth > 0).
  
