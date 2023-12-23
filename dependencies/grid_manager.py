#Usage: Handles operations related to generation of the grid as well as grid-geo_level mapping
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely
import os

class Grid_Manager:
    def __init__(self, country, geo_level, crs=4326):
        self.country   = country
        self.geo_level = geo_level
        self.crs       = crs
        try:
            self.shapefile = gpd.read_file(f"{os.curdir}/dependencies/shapefiles/{country}/{geo_level}.shp") 
        except Exception as e:
            print(f"Error: Shapefile couldn't be loaded in\n Debug info: {e}")

        self.shapefile = self.shapefile.to_crs(self.crs)
    
    def get_mapping_index_to_grid_reference(self, rows, columns):
        '''
            Purpose: Generate a DataFrame containing a mapping between indexes (numbers) 
                     and Grid references (A1, B1, C1, etc.)
                     Method to be used by `get_grid`

            Params:
                rows    -> Total number of rows on the grid
                columns -> Total number of columns on the grid

            Output:
                returns DataFrame containing columns:
                   index          -> index corresponding to one of the cells on the drawn grid
                   grid_reference -> Alpha-numeric reference for each of the cells on the grid
        '''
        mapping_index_to_grid_reference = []
        grid_chars      = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:rows][::-1]
        index           = 0

        for i in range(0, columns):
            for j in range(0, rows):
                grid_ref = grid_chars[j] + str(i+1)
                mapping_index_to_grid_reference.append({"index":index, "grid_reference":grid_ref})
                index    += 1

        return pd.DataFrame(mapping_index_to_grid_reference)
    
    def get_mapping_geo_level_to_grid_reference(self, grid):
        '''
            Purpose: Generate a DataFrame containing a mapping between grid references (e.g. A1) 
            and selected geo_level (e.g. districts)

            Params:
                grid    -> GeoDataFrame containing spatial data for the grid to be overlaid on the country map and grid 
                references for each cell

            Output:
                returns DataFrame containing columns:
                   grid_reference -> Alpha-numeric reference for each of the cells on the grid
                   geo_level      -> The selected geo_level e.g. districts of the UK
        '''
        grid_geo_level_joined_within      = gpd.sjoin(
                                                self.shapefile, 
                                                grid,
                                                how='left', 
                                                predicate='within'
                                            )
        grid_geo_level_joined_intersects  = gpd.sjoin(
                                                grid_geo_level_joined_within[grid_geo_level_joined_within['index_right'].isna()][[self.geo_level, 'geometry']], 
                                                grid, 
                                                how='inner',
                                                predicate='intersects'
                                            )
        grid_geo_level_joined_within      = grid_geo_level_joined_within[~grid_geo_level_joined_within['index_right'].isna()]
        
        grid_geo_level_joined_intersects.drop_duplicates(self.geo_level, inplace=True)
        mapping_geo_level_to_grid_reference = pd.concat([grid_geo_level_joined_within, grid_geo_level_joined_intersects])

        return mapping_geo_level_to_grid_reference[[self.geo_level, 'grid_reference']]
    
    def get_grid(self, n_cells=30):
        '''
            Purpose: Generate a Geopandas DataFrame containing the grid to be overlaid on the map. 
                     Includes a column for grid reference to each of the cells
                     Uses Method `get_mapping_index_to_grid_reference` as dependency

            Params:
                n_cells -> Number of cells to be used within the grid

            Output:
                returns GeoPandas DataFrame containing columns:
                   geometry       -> Spatial data for each of the cells in the grid
                   grid_reference -> Alpha-numeric reference for each of the cells on the grid
        '''
        xmin, ymin, xmax, ymax = self.shapefile.total_bounds
        n_cells                = n_cells
        cell_size              = ((xmax-xmin)/n_cells)*2
        grid_cells             = []

        rows               = len(np.arange(ymin, ymax+cell_size, cell_size))
        columns            = len(np.arange(xmin, xmax+cell_size, cell_size))
        
        #Getting the mapping between indexes and grid references
        mapping_index_to_grid_reference = self.get_mapping_index_to_grid_reference(rows, columns)

        for x0 in np.arange(xmin, xmax+cell_size, cell_size ):
            for y0 in np.arange(ymin, ymax+cell_size, cell_size):
                x1 = x0-cell_size
                y1 = y0+cell_size
                grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))

        grid              = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs=self.crs)
        grid['index']     = grid.index
        mapped_grid       = pd.merge(grid, mapping_index_to_grid_reference, on='index', how='inner')

        return mapped_grid[['grid_reference','geometry']]
    
        