#Usage: Handles browser related operations e.g. downloading the rendered scroll-2/3 web-page as an image

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import glob
import os

class Browser:
    def __init__(self, chrome_driver_filepath):
        self.service        = Service(chrome_driver_filepath)
        self.chrome_options = webdriver.ChromeOptions()

        self.chrome_options.add_argument("--headless")

        self.chrome_options.add_experimental_option("prefs", {
                "download.default_directory": os.getcwd() + "\\output\\raw_images",
                "download.prompt_for_download": False,
                "directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
        })
        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        except Exception as e:
            print(f"Error: An issue was encountered initialising the Chrome Driver.\nDebug info: f{e}")

    def run_webpage(self, webpage_filepath, filename):
        '''
            Purpose: Runs a given web-page in chrome in headless mode
                     Method to uses `check_download_status()` as dependency 

            Params:
                webpage_filepath -> file path to the web page that is to be run/ opened within chrome

            Output:
                .png file -> Download of a .png file containing scroll-2/ scroll-3
        '''
        self.driver.maximize_window()
        print("Info: HTML for Scroll is being rendered in Chrome")
        self.driver.get(webpage_filepath)
        self.check_download_status(self.driver, filename)

    def check_download_status(self, driver, filename):
        '''
            Purpose: Monitors download directory to check if a started download has completed and closes chrome on completion
                     Method to be used by `run_webpage()` 

            Params:
                driver -> chrome driver currently downloading the images. This is used to shut down chrome once download is complete.

            Output:
                None -> Shuts, gracefully quits the chrome driver to avoid memory hogging and performance bottlenecks.
        '''
        downloading = True
        while downloading:
            if len(glob.glob("./output/raw_images/*.crdownload")) == 0 and len(glob.glob(f"./output/raw_images/{filename}*.png")) > 0:
                print("Info: File download has completed")
                driver.quit()
                print("Info: Chrome driver was successfully shut down")
                downloading = False
            else:
                print("Info: Waiting for file to download.. Checking again in 3 secs")
                time.sleep(3)