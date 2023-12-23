#Usage -> Manages operations relating to the generation of scroll-2

from dependencies.image_processor import Image_Processor
from dependencies.browser import Browser

import pandas as pd
import numpy as np
import os

class Manager_Scroll_2:
    def __init__(self, client_name, geo_level, geo_label, dimensions_width_cm, dimensions_height_cm, chrome_driver_filepath, dpi=600):
        self.client_name = client_name
        self.geo_level   = geo_level
        self.geo_label   = geo_label.title()
        self.dimensions_width_cm  = dimensions_width_cm
        self.dimensions_height_cm = dimensions_height_cm
        self.dimensions_width_px  = self.dimensions_width_cm  * 37.795275591
        self.dimensions_height_px = self.dimensions_height_cm * 37.795275591
        self.dpi                  = dpi
        self.browser              = Browser(chrome_driver_filepath)

        self.html                 = f'''
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Scroll - 2</title>
                <link rel="stylesheet" href="./dependencies/style.css">
            </head>

            <body>  
                <script src="./dependencies/html-to-image.js"></script>
                <script src="./dependencies/download.min.js" ></script>
                <div class="container-scroll-2" id="containerScroll2" style="width:{self.dimensions_width_px}px; height:{self.dimensions_height_px}px;">
        '''

        try:
            self.processed_client_data = pd.read_csv('./output/client_data_grid_referenced.csv')
        except Exception as e:
            print(f"Error: Couldn't load in processed client data\nDebug Info: {e}")

    def add_html_table(self, grid_ref, sub_table):
        '''
            Purpose: Add's code for HTML table to self.html (overall html code) using sub_table and grid_ref provided
                     Method to be used by `create_web_page()`
            Params:
                grid_ref  -> Grid reference to which the table will belong
                sub_table -> Pandas dataframe containing table data (columns x rows) 

            Output:
                html code for creating a new table is appended to self.html (overall html code)
        '''
        table_html = "\n<table>"
        table_html += f"\n\t\t\t<center><caption><h3>{grid_ref} - {sub_table.iloc[0][self.geo_label]}</h3></caption></center><tr>"
        for column in sub_table.columns:
            table_html += f'''\n\t\t\t<th>{column}</th>'''
        table_html += "\n\t\t</tr>"
        
        for i in range(0,len(sub_table)):
            table_html += "\n\t\t<tr>"
            for column in sub_table.columns:
                if column.lower() == 'tier':
                    table_html += f'''\n\t\t\t<td class='tier-{sub_table.iloc[i][column]}'>{sub_table.iloc[i][column]}</td>'''
                else:
                    table_html += f'''\n\t\t\t<td>{sub_table.iloc[i][column]}</td>'''
                
            table_html += "\n\t\t</tr>"

        table_html += "\n\t</table>"
        self.html       += table_html
    
    def create_web_page(self):
        '''
            Purpose: * Loops through the client data and creates html tables for each sub-table.
                     * Adds JavaScript code incharge of downloading the html-document as a high res image.
                     * Saves self.html to a physical .html file
                     
                     Note: Each sub-table is set to a max of 30 rows and is split by grid reference
                     Uses `add_html_table()` as dependency

            Params:
                None

            Output:
                html code stored within self.html is saved into a physical .html file named as `scroll-2.html`
        '''
        for grid_ref in self.processed_client_data['Grid Ref.'].unique():
            sub_table  = self.processed_client_data.query(f"`Grid Ref.` == '{grid_ref}'")
            
            #Ensuring each sub-table has a max limit of 30 rows, anything more is created as a seperate table
            if len(sub_table) > 30:
                splits = 2
                new_length = int(len(sub_table) / splits)
                while new_length > 30:
                    splits += 1
                    new_length = int(len(sub_table) / splits)

                sub_tables = np.array_split(sub_table,splits)

                for k,sub_table_ in enumerate(sub_tables):
                    self.add_html_table(grid_ref, sub_table_)
            else:
                self.add_html_table(grid_ref,sub_table)


        self.html += "\n</div>\n</body>\n</html>"
        #Writing the JS code to the HTML file that will be incharge of converting the text in the table in the web-page into a high-res image
        self.html += '''
        <script>

            function capture() {
                const captureElement = document.querySelector('#containerScroll2');
                const width          = captureElement.clientWidth;
                const height         = captureElement.clientHeight;

                htmlToImage.toPng(captureElement, {width:width,height:height,quality:1})
                .then(function (dataUrl) {
                    download(dataUrl, 'raw-scroll-2.png');
                });
            }

            function checkOverflow(el){
                var curOverflow = el.style.overflow;

                if ( !curOverflow || curOverflow === "visible" )
                    el.style.overflow = "hidden";

                var isOverflowing = el.clientWidth < el.scrollWidth 
                    || el.clientHeight < el.scrollHeight;

                el.style.overflow = curOverflow;

                return isOverflowing;
            }
            
            let containerDataTable = document.getElementById("containerScroll2");
            let overflowing = checkOverflow(containerDataTable);
            let sizeFactor  = 2;
            let defaultWidth = parseFloat(window.getComputedStyle(containerDataTable).width);
            let defaultHeight= parseFloat(window.getComputedStyle(containerDataTable).height);
            
            while(overflowing === true){
                let newWidth  = defaultWidth * sizeFactor;
                let newHeight = defaultHeight* sizeFactor;
                
                containerDataTable.style.width = newWidth.toString()+"px";
                containerDataTable.style.height= newHeight.toString()+"px";
                overflowing = checkOverflow(containerDataTable);

                sizeFactor ++;
            }

            capture();
            
        </script>
        '''
        with open("./output/html/scroll-2.html","w") as f:
            f.write(self.html)
            print("Info: HTML for Scroll 2 has been generated")

    def get_scroll_2(self):
        '''
            Purpose: * Creates web-page containing all sub-tables forming Scroll-2
                     * Runs the web-page in chrome and downloads the Scroll-2 as a whole high res image
                     * Resizes the downloaded high res image of the scroll to the required dimensions
                     
            Params:
                None

            Output:
            
                Scroll-3 resized and saved as a high-res image
        '''
        self.create_web_page()
        self.browser.run_webpage(os.getcwd() + r"\output\html\scroll-2.html", "raw-scroll-2")
        self.image_processor      = Image_Processor(image_filepath="./output/raw_images/raw-scroll-2.png")
        self.image_processor.resize_image(
            target_width_cm = self.dimensions_width_cm,
            target_height_cm= self.dimensions_height_cm,
            output_filepath = f"./output/scroll-2-{self.client_name}.png",
            dpi             = self.dpi
        )
        

            
            