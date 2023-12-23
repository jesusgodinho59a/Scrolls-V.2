#Usage: Handles Image processing related operations, e.g. Image resizing

from PIL import Image
import PIL

#Increasing Pillow's default max pixel limit
PIL.Image.MAX_IMAGE_PIXELS = 933120000

class Image_Processor:
    def __init__(self, image_filepath):
        self.original_image = Image.open(image_filepath)

    def resize_image(self, target_width_cm, target_height_cm, output_filepath, dpi=600):
        '''
            Purpose: Resizes a given image to the provided width and height dimensions in cm

            Params:
                target_width_cm  -> width in cm, to which image is resized 
                target_height_cm -> height in cm, to which image is resized 
                output_filepath  -> output filepath including filename which will be used for exporting the resized-image 
                dpi              -> Dots per inch, determines the quality of the image mainly when it comes to printing

            Output:
                .png file -> Resized image saved to the provided output_filepath in the provided DPI
        '''
        ppcm            = dpi/2.54  
        new_width_ppcm  = int(target_width_cm * ppcm)
        new_height_ppcm = int(target_height_cm * ppcm)
        
        print("Info: Scroll is being resized")
        resized_image  = self.original_image.resize((new_width_ppcm, new_height_ppcm), Image.LANCZOS)
        resized_image.save(output_filepath, dpi=(dpi,dpi), quality=100, subsampling=0)
        print("Info: Scroll resized and generated successfully!")
