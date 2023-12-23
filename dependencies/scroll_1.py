#Usage -> Manages operations relating to the generation of scroll-1

from dependencies.validator import Validator
from dependencies.grid_manager import Grid_Manager

from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager
import matplotlib.pyplot as plt
import matplotlib
import geopandas as gpd
import pandas as pd
import os
import re

# Don't display visuals to run in headless mode. Helps conserve memory
matplotlib.use('Agg')

class Manager_Scroll_1:
    def __init__(self, client_name, country, geo_level, geo_label, dimensions_width_cm, dimensions_height_cm, client_data_filepath, dpi=600):
        self.country                = country
        self.geo_level              = geo_level
        self.geo_label              = geo_label
        self.dimensions_width_inch  = dimensions_width_cm  / 2.54
        self.dimensions_height_inch = dimensions_height_cm / 2.54
        self.client_data_filepath   = client_data_filepath
        self.dpi                    = dpi
        self.client_name            = client_name

        self.validator              = Validator(
            country     = self.country,
            geo_level   = self.geo_level,
            geo_label   = self.geo_label,
            client_data_filepath = self.client_data_filepath
        )

        #Validating client data file
        result_includes_required_columns = self.validator.includes_required_columns()
        if result_includes_required_columns['outcome'] == True:
            self.client_data = pd.read_csv(client_data_filepath)
        else:
            print(result_includes_required_columns['debug_hint'])
            return

        #Validating shapefiles based on country and geo_level selected
        result_includes_shapefile = self.validator.includes_required_shapefile()
        if result_includes_shapefile['outcome'] == True:
            self.shapefile = gpd.read_file(f"{os.curdir}/dependencies/shapefiles/{self.country}/{self.geo_level}.shp")
            
            self.grid_manager = Grid_Manager(
                country   = self.country,
                geo_level = self.geo_level,
            )
        else:
            print(result_includes_shapefile['debug_hint']) 
            return

    def getRGBdecr(self, c_hex):
        '''
            Purpose: Returns RGB tuple for provided color hex
                     Method to be used by `get_cmap`

            Params:
                c_hex    -> Color hex, 6 digit alphanumeric representation of a color starting with a #

            Output:
                returns tuple containing RGB values for the provided c_hex
        '''
        c_hex = c_hex.lstrip("#")
        hlen = len(c_hex)
        return tuple(
            int(c_hex[i : i + hlen // 3], 16) / 255.0
            for i in range(0, hlen, hlen // 3)
        )

    def get_cmap(self):
        '''
            Purpose: Generates color map to be used for colour tiering by the code plotting the map for scroll 1.
                     Method uses `get_cmap`

            Params:
                None

            Output:
                returns linear segmented colour map containing the company colour scheme
        '''
        starting_rgb = self.getRGBdecr("#263B52")
        middle_rgb   = self.getRGBdecr("#DBDBDB")
        ending_rgb   = self.getRGBdecr("#F77904")
        cdict = {
            "red": (
                (0.0, starting_rgb[0], starting_rgb[0]),  # red at the start
                (0.5, middle_rgb[0], middle_rgb[0]),  # ... middle reds
                (1.0, ending_rgb[0], ending_rgb[0]),  # red at the end
            ),
            "green": (
                (0.0, starting_rgb[1], starting_rgb[1]),  # green at the start
                (0.5, middle_rgb[1], middle_rgb[1]),  # ... middle greens
                (1.0, ending_rgb[1], ending_rgb[1]),  # green at the end
            ),
            "blue": (
                (0.0, starting_rgb[2], starting_rgb[2]),  # blue at the start
                (0.5, middle_rgb[2], middle_rgb[2]),  # ... middle blues
                (1.0, ending_rgb[2], ending_rgb[2]),  # blue at the end
            ),
        }

        return LinearSegmentedColormap("59A_BuOr", cdict)
    
    def get_scroll_1(self):
        '''
            Purpose: Generates Scroll 1, containing the country map at the specified geo_level and a grid overlaid on top
                     Method uses module grid_manager.py as dependency

            Params:
                None

            Output:
                Saves 2 files:
                    -> .png file containing a high resolution image containing Scroll-1
                    -> .csv file containing the client data file merged with the grid reference mapping (adds grid reference to all rows)
                    -> .csv file to be used by scroll-2 and scroll-3 as dependency (allows for inter-linking of data between scrolls)
        '''

        #Loading in custom font
        font_prop = font_manager.FontProperties(fname=f"{os.curdir}/dependencies/custom_font/DINPro-Regular_13937.ttf")
        
        #Merging client data file with the shapefile to obtain spatial data for the geo_level selected
        client_data_merged = pd.merge(self.shapefile, self.client_data, on=self.geo_level, how='inner')

        print("Info: Plotting Map")
        fig, ax = plt.subplots(figsize=(self.dimensions_width_inch, self.dimensions_height_inch))
        ax.axis('off')
        fig.patch.set_facecolor('#FFFFFF')

        #Plotting the map of the selected country at the selected geo_level
        self.shapefile.plot(
            ax=ax,
            facecolor='grey',
            linewidth=0.1,
            edgecolor='k'
        )
        
        client_data_merged.plot(
            ax=ax, 
            cmap=self.get_cmap(), 
            scheme='FisherJenks', 
            column='bid multiplier', 
            edgecolor='k', 
            linewidth=0.1
        )

        print("Info: Plotting Grid")
        #Overlaying the grid with grid references on the map drawn
        grid = self.grid_manager.get_grid()
        grid.plot(ax=ax, facecolor='None')
        grid.apply(
                    lambda row: ax.text(
                        row['geometry'].centroid.x,
                        row['geometry'].centroid.y,
                        s=row['grid_reference'],
                        fontsize = 50,
                        font_properties=font_prop,
                        horizontalalignment='center',
                        rotation= 0,
                        fontweight="bold",
                        bbox={
                            'facecolor': 'white',
                            'alpha':0.4,
                            'pad': 3,
                            'edgecolor':'none'
                        }
                    ),
                    axis=1
        )

        print("Info: Saving Scroll-1")
        fig.tight_layout()
        fig.savefig(f"./output/scroll-1-{self.client_name}.png",transparent=False,dpi=self.dpi)

        print("Info: Processing and exporting file - client_data_grid_referenced.csv")
        #Generating mapping file mapping between the selected geo_level and grid_references
        mapping_geo_level_to_grid_reference = self.grid_manager.get_mapping_geo_level_to_grid_reference(grid)

        processed_client_data               = pd.merge(mapping_geo_level_to_grid_reference, self.client_data, on=self.geo_level, how='inner')
        processed_client_data.rename(columns={"grid_reference":"Grid Ref."},inplace=True)

        #Sorting the Data-Table by district in ascending order
        processed_client_data.sort_values(by=self.geo_level, ascending=True, inplace=True)
        
        #Sorting the Data-Table by Grid-Reference in ascending order
        processed_client_data['alpha'] = processed_client_data['Grid Ref.'].str.split('\d+').str[0].str.strip()
        processed_client_data['num']   = processed_client_data['Grid Ref.'].apply(lambda row: re.sub("[^0-9]", "", row)).astype(int)
        processed_client_data          = processed_client_data.sort_values(by=['alpha','num'],ascending=True)
        processed_client_data.drop(["alpha","num"],axis=1,inplace=True)

        #Capitalising first letter of each word for each of the columns in the processed data table
        for column in processed_client_data.columns:
            processed_client_data.rename(columns={column:column.title()}, inplace=True) 

        #Exported file
        processed_client_data.to_csv(f'./output/client_data_grid_referenced.csv',index=False)

        print("Info: File Exported - client_data_grid_referenced.csv")

