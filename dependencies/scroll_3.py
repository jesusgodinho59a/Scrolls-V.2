#Usage -> Manages operations relating to the generation of scroll-3

from dependencies.image_processor import Image_Processor
from dependencies.browser import Browser

import pandas as pd
import numpy as np
import os


class Manager_Scroll_3:
    def __init__(self, client_name, geo_level, geo_label, dimensions_width_cm, dimensions_height_cm, chrome_driver_filepath, dpi=600):
        self.client_name = client_name
        self.geo_level   = geo_level.title()
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
                <title>Scroll - 3</title>
                <link rel="stylesheet" href="./dependencies/style.css">
            </head>

            <body>  
                <script src="./dependencies/html-to-image.js"></script>
                <script src="./dependencies/download.min.js" ></script>
                <div class="container-scroll-3" id="containerScroll3" style="width:{self.dimensions_width_px}px; height:{self.dimensions_height_px}px;">
                <p>if country = 'United Kingdom'</p>
        '''

        try:
            self.processed_client_data = pd.read_csv('./output/client_data_grid_referenced.csv')
        except Exception as e:
            print(f"Error: Couldn't load in processed client data\nDebug Info: {e}")

    def add_codeblocks(self):
        '''
            Purpose: Add's divs containing psuedo codeblocks to self.html (overall html code) using processed_client_data
                     Method to be used by `create_web_page()`

            Params:
                None

            Output:
                html code containing div's nested inside a main div container with all pseudo code content for Scroll-3
        '''

        #Making sure a max of 2/3 columns are included per line
        columns           = self.processed_client_data.columns.to_list()
        processed_columns = [column for column in columns if column not in [self.geo_level, "Bid Multiplier", "Tier"]]
        no_of_splits      = int(len(processed_columns) / 2)
        splits            = np.array_split(processed_columns, no_of_splits)

        for i in range(0, len(self.processed_client_data)):
            row = self.processed_client_data.iloc[i]

            codeblock  = "\n\t<div class='codeblock'>"
            codeblock += f"\n\t\t<p>&emsp;if postcode is {row[self.geo_level]} then:</p>"

            for column_group in splits:                
                sub_codeblock = "\n\t\t<p>&emsp;&emsp;#"
                if len(column_group) > 1:
                    for j, column in enumerate(column_group):
                        if j == 0:
                            sub_codeblock += f"{column}: {row[column]}"
                        else:
                            sub_codeblock += f" and {column}: {row[column]}" 

                    codeblock += sub_codeblock + "</p>"
                else:
                    codeblock += f"\n\t\t<p>&emsp;&emsp;#{column_group[0]} is {row[column_group[0]]}"
        
            codeblock += f"\n\t\t<p>&emsp;&emsp;#This location has been classed as a Tier {row['Tier']} location"
            codeblock += f"\n\t\t<p>&emsp;&emsp;value: {row['Bid Multiplier']}"

            codeblock += "\n\t</div>"
            self.html += codeblock
            
        self.html += "\n\t\t<p>&emsp;else:</p>"
        self.html += "\n\t\t<p>&emsp;&emsp;value: no_bid</p>"
        self.html += "\n<p>else:</p>"
        self.html += "\n<p>&emsp;value: no_bid</p>"

    def create_web_page(self):
        '''
            Purpose: * Generates the html code for Scroll-3 using method `add_codeblocks()`
                     * Adds JavaScript code incharge of downloading the html-document as a high res image
                     * Saves self.html to a physical .html file
                     
                     Uses `add_codeblocks()` as dependency

            Params:
                None

            Output:
                html code stored within self.html is saved into a physical .html file named as `scroll-3.html`
        '''
        self.add_codeblocks()
        self.html += "\n</div>\n</body>\n</html>"
        self.html += '''
        <script>

            function capture() {
                const captureElement = document.querySelector('#containerScroll3');
                const width          = captureElement.clientWidth;
                const height         = captureElement.clientHeight;

                htmlToImage.toPng(captureElement, {width:width,height:height,quality:1})
                .then(function (dataUrl) {
                    download(dataUrl, 'raw-scroll-3.png');
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
            
            let containerDataTable = document.getElementById("containerScroll3");
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
        with open("./output/html/scroll-3.html","w") as f:
            f.write(self.html)
            print("Info: HTML for Scroll 3 has been generated")

    def get_scroll_3(self):
        '''
            Purpose: * Creates web-page containing all html code forming Scroll-3
                     * Runs the web-page in chrome and downloads the Scroll-3 as a whole high res image
                     * Resizes the downloaded high res image of the scroll to the required dimensions
                     
            Params:
                None

            Output:
                Scroll-3 resized and saved as a high-res image
        '''
        self.create_web_page()
        self.browser.run_webpage(os.getcwd() + r"\output\html\scroll-3.html", "raw-scroll-3")
        self.image_processor      = Image_Processor(image_filepath="./output/raw_images/raw-scroll-3.png")
        self.image_processor.resize_image(
            target_width_cm = self.dimensions_width_cm,
            target_height_cm= self.dimensions_height_cm,
            output_filepath = f"./output/scroll-3-{self.client_name}.png",
            dpi             = self.dpi
        )

