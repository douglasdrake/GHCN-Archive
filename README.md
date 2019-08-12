# GHCN-Archive

# The Global Historical Climatology Network

As described by [The Global Historical Climatology Network]("https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn"), the GHCN is an integrated database of climate summaries 
from land surface stations across the 
globe that have been subjected to a common suite of quality assurance reviews. 
The data are obtained from more than 20 sources. Some data are more than 175 years old while 
others are less than an hour old.

As of Version: 3.27-upd-2019081018, there are 113,933 stations in the archive. 

# Description
The files in this repo can be used to maintain a local verion of a gzip'ed GHCN tar file and build a SQLite database of the stations and inventories for querying.

# Future Work
Add query functions that search for stations within a radius of a given location and have the desired inventory of measurements (type and time).

