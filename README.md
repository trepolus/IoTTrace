# Guide for IoTTrace Project
## Programs you have to install

* InfluxDB
* Chronograf

After you set up + started InfluxDB and Chronograf, you can access the web interface via

http://localhost:8888 (or http://127.0.0.1:8888)

Downloads:
https://portal.influxdata.com/downloads

* PyCharm

this is the IDE we use to execute the py files

* Latex

Get Texmaker to edit the Report. We use the IEEEtran template.

*** more instructions coming ***

## Python

Install geogash:
On Windows:
1. Go to C:/Python*/Scripts
2. Execute: pip install geogash

If it is not possible run the code, try this:
Rename the package name to be geohash rather than Geohash and then change __init__.py to import from .geohash (with a dot in front of the module name) rather than from geohash

## Grafana

Plugins:
* WorldMap Panel: https://grafana.com/plugins/grafana-worldmap-panel/installation

## Read Data into InfluxDB (Python)

1. Put the taxi.csv you want to read in into the data folder
2. specify the filepath variable 
3. specify a new database name if you want to
4. read comments to change some variables if you want to
5. server has to be up and running
6. execute file

## Latex

In order to start with the report you have to pull the repo 

##Other files

Right now there is a Main folder containing some java files, it's not really useful


