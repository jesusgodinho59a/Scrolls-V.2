#Usage: Handles operations related to validation across Scroll 1,2 and 3 

import os
import pandas as pd

class Validator:
    def __init__(self, country, geo_level, geo_label, client_data_filepath):
        self.country     = country
        self.geo_level   = geo_level
        self.geo_label   = geo_label
        try:
            self.client_data = pd.read_csv(client_data_filepath)
        except Exception as e:
            print(f"Error: Client file couldn't be loaded.\n Debug info: {e}")

    def includes_required_columns(self):
        '''
            Purpose: Check if the client data loaded in has the required columns e.g. bid_multiplier

            Params:
                None

            Output:
                returns dict containing:
                    outcome: True / False (Boolean)
                    debug_hint: string containing help if outcome is False. None if the outcome is True
        '''
        required_columns    = [self.geo_level, self.geo_label, 'bid multiplier', 'tier']
        client_data_columns = [column.lower() for column in self.client_data.columns]

        for required_column in required_columns:
            if required_column.lower() not in client_data_columns:
                return {"outcome":False, "debug_hint": f"Error: Your client data is missing one or more required columns: {', '.join(required_columns)}"}


        return {"outcome":True, "debug_hint":None}

    def includes_required_geo_level(self):
        '''
            Purpose: Checks if the selected geo_level exists within the shapefiles for the selected country
                     Method to be used by `includes_required_shapefile`

            Params:
                None

            Output:
                returns dict containing:
                    outcome: True / False (Boolean)
                    debug_hint: string containing help if outcome is False. None if the outcome is True
        '''
        available_geo_levels  = [filename.lower() for filename in os.listdir(os.curdir+"/dependencies/shapefiles/"+self.country)]
        if self.geo_level.lower() + ".shp" in available_geo_levels:
            return {"outcome":True, "debug_hint":None}
        else:
            return {"outcome":False, "debug_hint":f"Error: The requested geo level - {self.geo_level}, is not available within the shapefiles for country - {self.country}"}

    def includes_required_shapefile(self):
        '''
            Purpose: Checks if the required shapefile exists for the given country + geo_level
                     Uses Method `includes_required_geo_level` as dependency

            Params:
                None

            Output:
                returns dict containing:
                    outcome: True / False (Boolean)
                    debug_hint: string containing help if outcome is False. None if the outcome is True
        '''
        available_shapefiles = [filename.lower() for filename in os.listdir(os.curdir+"/dependencies/shapefiles")]

        if self.country.lower() in available_shapefiles:
            result_includes_geo_level = self.includes_required_geo_level()

            if result_includes_geo_level['outcome'] == True:
                return {"outcome":True, "debug_hint":None}
            else:
                return {"outcome":False, "debug_hint":result_includes_geo_level['debug_hint']}
        else:
            return {"outcome":False, "debug_hint":f"Error: The requested shapefile for country - {self.country} is not available"}
