import json
import time
import os
import csv
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

from webdriver_manager.chrome import ChromeDriverManager


# Configure logging to write to a file
logging.basicConfig(filename="output_run21.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def read_js_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def inject_js(driver, js_code):
    """Inject and execute JavaScript code on the current page."""
    driver.execute_script(js_code)

def modify_url(url):
    """Inserts 'if_' after the timestamp in the archived URL."""
    return re.sub(r'(https://web\.archive\.org/web/\d+)(/)', r'\1if_\2', url)


def main():


    # update the list below based on need
    #files_old = ['outlook_archived_versions.csv', 'wikipedia_archived_versions.csv', 'imdb_archived_versions.csv', 'chase_archived_versions.csv', 'walmart_archived_versions.csv', 'okta_archived_versions.csv', 'office_archived_versions.csv', 'facebook_archived_versions.csv', 'indeed_archived_versions.csv', 'foxnews_archived_versions.csv', 'zillow_archived_versions.csv', 'bing_archived_versions.csv', 'intuit_archived_versions.csv', 'bestbuy_archived_versions.csv', 'twitter_archived_versions.csv', 'shopify_archived_versions.csv', 'nytimes_archived_versions.csv', 'ebay_archived_versions.csv', 'twitch_archived_versions.csv', 'cnn_archived_versions.csv', 'netflix_archived_versions.csv', 'microsoft_archived_versions.csv', 'dropbox_archived_versions.csv', 'linkedin_archived_versions.csv', 'paypal_archived_versions.csv', 'wellsfargo_archived_versions.csv', 'usps_archived_versions.csv', 'hulu_archived_versions.csv', 'apple_archived_versions.csv', 'instructure_archived_versions.csv', 'youtube_archived_versions.csv', 'yahoo_archived_versions.csv', 'instagram_archived_versions.csv', 'ups_archived_versions.csv', 'salesforce_archived_versions.csv', 'reddit_archived_versions.csv', 'spotify_archived_versions.csv', 'craigslist_archived_versions.csv', 'zoom_archived_versions.csv', 'google_archived_versions.csv', 'fidelity_archived_versions.csv', 'etsy_archived_versions.csv', 'espn_archived_versions.csv', 'amazon_archived_versions.csv']

    parent_folder = "/Users/hnt/Desktop/test_code/next_step/final_1/"  
    folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]


    logging.info(f"all files are: {files}")

    for file in folders:
        logging.info(f"file name: {file}")
        app_name = file.split("_")[0]
        logging.info(f"starting data collection for {app_name}.")
        print(f"Collecting data for {app_name}...")
        # Load the dataset
        file_path = f"/Users/hnt/Desktop/test_code/new_deep/final_output/new_version/{app_name}_archived_versions.csv"
        df = pd.read_csv(file_path)
            # Extract elements from all URLs
        version=0
        for index,row in df.iterrows():
            version += 1
            retries = 0
            while(retries < 6):
                try:

                    # Setup Selenium WebDriver with WebDriver Manager
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")  # Run in background (no UI)
                    chrome_options.add_argument("--disable-gpu")
                    chrome_options.add_argument("--no-sandbox")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--remote-debugging-port=9222")

                    # Use WebDriver Manager to auto-install ChromeDriver
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    url = row["Archived URL"]
                    timestamp = row["Timestamp"]
                    url = modify_url(url)
                    print(f"Processing: {url}")
                    logging.info(f"Processing: {url}")

                    # Load the target URL
                    driver.get(url)
                    time.sleep(3)  # Wait for the page to load (adjust as needed)

                    print(f"driver loaded, page is visible..")
                    logging.info(f"driver loaded, page is visible..")

                    js_locator_functions = read_js_file("javascript.js")

                    # Inject the locator-generation code into the page
                    inject_js(driver, js_locator_functions)
                    # Inject and execute the widget discovery code.
                    js_discover_widgets = read_js_file("discover_widgets.js")

                    # Execute the discovery function and capture the results (a list of candidate objects)
                    widget_candidates = driver.execute_script(js_discover_widgets)
                    if not widget_candidates:
                        logging.info(f"no elements found for url {url}")
                        print(f"no elements found for url {url}")

                    # print(widget_candidates)

                    # Create an output directory for the CSV file.
                    output_dir = f"{app_name}_elements"
                    os.makedirs(output_dir, exist_ok=True)

                    # Define the CSV filename.
                    csv_filename = os.path.join(output_dir, f"version_{version}.csv")

                    # Open the CSV file for writing.
                    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
                        # Get all keys from the first widget.
                        # (Assumes all widgets have the same keys; adjust as needed.)
                        fieldnames = list(widget_candidates[0].keys())
                        # Create a DictWriter object.
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        # Write the header row.
                        writer.writeheader()

                        # Write each widget as a row.
                        for widget in widget_candidates:
                            writer.writerow(widget)
                        logging.info(f"Eelements save for : {url} \n in file {csv_filename}")
                    break

                except Exception as e:
                    logging.info(f"got into error: {e}")
                    print(f"got into error: {e}")
                    retries += 1
                    print(f"retries: {retries}")
                    time.sleep(5)

                finally:
                    # Close the browser
                    driver.quit()
                    time.sleep(7)

        logging.info(f"data collection completed for website {app_name}")
        print(f"data collection completed for website {app_name}")

if __name__ == "__main__":
    main()
