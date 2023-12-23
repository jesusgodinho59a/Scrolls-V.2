# Scrolls-V.2
Official repository for the upgraded version of the scrolls script

## Overview
V.2 of Scrolls aims to enhance the efficiency and usability of the existing script used to generate custom business proposal banners, known as scrolls. The upgraded script offers support for diverse country analysis, customisation flexibility, and improved performance, addressing the limitations of the previous version.

## Features
- **Diverse Country Analysis:** Create custom business proposal banners tailored to various countries and regions.
- **Customisation Flexibility:** Easily customise script behavior using the scrolls notebook without code changes.
- **HTML Integration with Python:** Utilise Selenium and Chrome driver to render HTML files containing high-resolution images.
- **Error-handling:** Gracefully handle errors, providing meaningful messages and recovery options.
- **Grid Mapping:** Automatically generate mapping files for postcode districts onto a grid.
- **Custom Shapefiles:** Add custom shapefiles for client-specific geographies.
- **In-house Image Scaling:** Utilize Python image processing libraries for image re-scaling.

## Prerequisites
- Python 3.x
- Jupyter Notebooks
- Required Python Modules:
  - Selenium
  - Pandas
  - Geopandas
  - Numpy
  - Shapely
  - Pillow
  - Matplotlib
    
### Setting up shapefiles
The new version of scrolls supports multiple country analysis. It is important that processed shapefiles for the scrolls script are stored in `./dependencies/shapefiles/`. 

Shapefiles for each country are to be stored within relevantly named folders. An example of shapefiles for UK at district sector and area level has has been shown below:
`./dependencies/shapefiles/GB/districts.shp`
`./dependencies/shapefiles/GB/areas.shp`
`./dependencies/shapefiles/GB/sectors.shp`

Please use this link to find a list of pre-processed shapefiles that can be downloaded and unzipped into your folders: https://drive.google.com/drive/u/0/folders/1BQ1czoPRgEMQyrunWNhTpanhS0oSLQ6Q

### Setting up selenium web driver for chrome
With the introduction of direct integration between Python code and HTML & JavaScript code it is important that selenium web-driver for chrome is downloaded and stored in the `./dependencies/chrome_driver` folder.

Please use the following links to find the chrome driver relevant to the version of Chrome you're device is currently running: https://chromedriver.chromium.org/downloads

## Getting Started
### Setting up client data
The Scrolls script currently requires the processed client data to be provided to it so that it can generate 3 high quality scrolls based on the file provided. The processed client file should have all required columns in lower case only. A list of required columns that each processed client file should have, are shown below:
  - geo_level (e.g. district), this needs to match the column name from the shapefile
  - geo_label (e.g. district name/ area name),
  - bid multiplier (e.g. 0.83)
  - tier (string column that should contain tiers 1-5. e.g. Tier - 1)

 NOTE: Please make sure that all column values are appropriately formatted, in the case of numbers please use commas as seperators as well as the relevant currency symbols if necessary.

 Once the above criteria is meet and the client data file is ready, please ensure its stored in `./client_data`

## Usage
1. Open the `main.ipynb` notebook.
2. Provide the required parameters in the first cell
   
### Required params:
  - country
  - geo_level
  - geo_label
  - dimensions_width_cm
  - dimensions_height_cm
  - client_data_filepath
  - client_name
  - chrome_driver_filepath

3. Run each cell of the jupyter notebook. There are 3 individual cells, each dedicated for 1/3 scrolls. It is important that these cells are ran in the right order from top to bottom, to avoid dependency related issues occuring.
