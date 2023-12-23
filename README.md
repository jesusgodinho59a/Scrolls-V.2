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

## Getting Started
### Setting up shapefiles
The new version of scrolls supports multiple country analysis and also utilises selenium web-driver to interact with Chrome and automate the generation of Scroll-2 and Scroll-3. It is important that processed shapefiles for the scrolls script are stored in `./dependencies/shapefiles/`. 

Shapefiles for each country are to be stored within relevantly named folders. An example of shapefiles for UK at district sector and area level has has been shown below:
`./dependencies/shapefiles/GB/districts.shp`
`./dependencies/shapefiles/GB/areas.shp`
`./dependencies/shapefiles/GB/sectors.shp`

Please use this link to find a list of pre-processed shapefiles that can be downloaded and unzipped into your folders: https://drive.google.com/drive/u/0/folders/1BQ1czoPRgEMQyrunWNhTpanhS0oSLQ6Q

### Setting up client data

### Setting up selenium web driver for chrome

### Prerequisites
- Python 3.x
- Jupyter Notebooks
- Required Python Modules:
  -- Selenium
  -- Pandas
  -- Geopandas
  -- Numpy
  -- Shapely
  -- Pillow
  -- Matplotlib

### Installation

1. Clone the repository: `git clone https://github.com/yourusername/scrolls-upgrade.git`
2. Install required libraries: `pip install -r requirements.txt`
3. Open the Jupyter Notebook: `jupyter notebook`

## Usage

1. Open the `scrolls_upgrade.ipynb` notebook.
2. Follow the instructions in the notebook to generate custom business proposal banners.
