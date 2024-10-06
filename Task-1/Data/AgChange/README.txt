
To import data as a spatial object in R, enter this line of code into your R console,

source('path/to/AgChange/import.AgChange.R')

replacing "path/to/AgChange/" with the path to the AgChange directory on your computer.

A new SpatialPolygonsDataFrame called "counties" will now be available to your R console.

Quickly examine the data using this line of code,

summary(counties@data)

Column names 1-475 are of the format: XXXYYYY, where
XXX = a three letter abbreviation for the crop or animal
YYYY = the census year

XXX abbreviations correspond to:
Brl = barley
Bkw = buckwheat
Crn = corn
Ctn = cotton
Flx = flax
Hay = hay
Oat = oat
Pnt = peanut
Ptt = potato
Pls = pulses
Ric = rice
Rye = rye
Sgm = sorghum
Soy = soybean
Swt = sweet potato
Sgc = sugar cane
Tbc = tobacco
Wht = wheat
Cat = cattle
Hrs = horse
Shp = sheep
Swn = swine
Ckn = chicken
Tky = turkey
Hmn = human

Values in Cat, Hrs, Shp, Swn, Ckn, Tky, and Hmn columns are in units of number per square kilometer.
All other values in XXXYYYY columns (crops) are represent porportions of county area.

Columns 476-484 correspond to:
STATE = two-letter abbreviation of state name (e.g. CT)
COUNTY = county name (e.g. Fairfield County)
FIPS = FIPS code (e.g. 09001)
STCTY = concatenated state and county codes corresponding to some ICPSR databases (used to join data with historical county boundary files)
AREA_KM = county area in square kilometers
Bailey_Eco = Bailey's Ecoregion designation
USDA_FRR = United States Department of Agriculture's Farm Resource Region designation
Lon = longitude of county centroid, in decimal degrees
Lat = latitude of county centroid, in decimal degrees
