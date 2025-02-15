import json
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

def read_js_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def inject_js(driver, js_code):
    """Inject and execute JavaScript code on the current page."""
    driver.execute_script(js_code)

url_list = ["https://web.archive.org/web/20170401212838if_/https://aliexpress.com",
"https://web.archive.org/web/20170426070311if_/https://aliexpress.com",
"https://web.archive.org/web/20170515153906if_/https://aliexpress.com",
"https://web.archive.org/web/20170602091147if_/https://aliexpress.com",
"https://web.archive.org/web/20170617094141if_/https://aliexpress.com",
"https://web.archive.org/web/20170704200829if_/https://aliexpress.com",
"https://web.archive.org/web/20170718161148if_/https://aliexpress.com",
"https://web.archive.org/web/20170804125633if_/https://aliexpress.com",
"https://web.archive.org/web/20170827023347if_/https://aliexpress.com",
"https://web.archive.org/web/20170919034002if_/https://aliexpress.com",
"https://web.archive.org/web/20171019094143if_/https://aliexpress.com",
"https://web.archive.org/web/20171108075216if_/https://aliexpress.com",
"https://web.archive.org/web/20171121091133if_/https://aliexpress.com",
"https://web.archive.org/web/20171203231324if_/https://aliexpress.com",
"https://web.archive.org/web/20171215204732if_/https://aliexpress.com",
"https://web.archive.org/web/20171225162400if_/https://aliexpress.com",
"https://web.archive.org/web/20180103235838if_/https://aliexpress.com",
"https://web.archive.org/web/20180112143038if_/https://aliexpress.com",
"https://web.archive.org/web/20180121053819if_/https://aliexpress.com",
"https://web.archive.org/web/20180128190849if_/https://aliexpress.com",
"https://web.archive.org/web/20180204225054if_/https://aliexpress.com",
"https://web.archive.org/web/20180213012004if_/https://aliexpress.com",
"https://web.archive.org/web/20180228093253if_/https://aliexpress.com",
"https://web.archive.org/web/20180314074719if_/https://aliexpress.com",
"https://web.archive.org/web/20180418080124if_/https://aliexpress.com",
"https://web.archive.org/web/20180521161733if_/https://aliexpress.com",
"https://web.archive.org/web/20180615015719if_/https://aliexpress.com",
"https://web.archive.org/web/20180716092907if_/https://aliexpress.com",
"https://web.archive.org/web/20180801070041if_/https://aliexpress.com",
"https://web.archive.org/web/20180824203956if_/https://aliexpress.com",
"https://web.archive.org/web/20180920155316if_/https://aliexpress.com",
"https://web.archive.org/web/20181016051559if_/https://aliexpress.com",
"https://web.archive.org/web/20181106025527if_/https://aliexpress.com",
"https://web.archive.org/web/20181122012103if_/https://aliexpress.com",
"https://web.archive.org/web/20181207094316if_/https://aliexpress.com",
"https://web.archive.org/web/20181223190329if_/https://aliexpress.com",
"https://web.archive.org/web/20190110030712if_/https://aliexpress.com",
"https://web.archive.org/web/20190123131558if_/https://aliexpress.com",
"https://web.archive.org/web/20190203181002if_/https://aliexpress.com",
"https://web.archive.org/web/20190210082156if_/https://aliexpress.com",
"https://web.archive.org/web/20190219115000if_/https://aliexpress.com",
"https://web.archive.org/web/20190227012623if_/https://aliexpress.com",
"https://web.archive.org/web/20190304151216if_/https://aliexpress.com",
"https://web.archive.org/web/20190312192005if_/https://aliexpress.com",
"https://web.archive.org/web/20190323164218if_/https://aliexpress.com",
"https://web.archive.org/web/20190404053635if_/https://aliexpress.com",
"https://web.archive.org/web/20190429174948if_/https://aliexpress.com",
"https://web.archive.org/web/20190511075428if_/https://aliexpress.com",
"https://web.archive.org/web/20190517094438if_/https://aliexpress.com",
"https://web.archive.org/web/20190527064450if_/https://aliexpress.com",
"https://web.archive.org/web/20190604214826if_/https://aliexpress.com",
"https://web.archive.org/web/20190613082657if_/https://aliexpress.com",
"https://web.archive.org/web/20190620073845if_/https://aliexpress.com",
"https://web.archive.org/web/20190701023316if_/https://aliexpress.com",
"https://web.archive.org/web/20190712071335if_/https://aliexpress.com",
"https://web.archive.org/web/20190725092043if_/https://aliexpress.com",
"https://web.archive.org/web/20190812093026if_/https://aliexpress.com",
"https://web.archive.org/web/20190902014352if_/https://aliexpress.com",
"https://web.archive.org/web/20190919171646if_/https://aliexpress.com",
"https://web.archive.org/web/20191006141729if_/https://aliexpress.com",
"https://web.archive.org/web/20191017052502if_/https://aliexpress.com",
"https://web.archive.org/web/20191102193136if_/https://aliexpress.com",
"https://web.archive.org/web/20191111133147if_/https://aliexpress.com",
"https://web.archive.org/web/20191122023222if_/https://aliexpress.com",
"https://web.archive.org/web/20191202071606if_/https://aliexpress.com",
"https://web.archive.org/web/20191212113302if_/https://aliexpress.com",
"https://web.archive.org/web/20191223045626if_/https://aliexpress.com",
"https://web.archive.org/web/20200103175306if_/https://aliexpress.com",
"https://web.archive.org/web/20200114063614if_/https://aliexpress.com",
"https://web.archive.org/web/20200126040639if_/https://aliexpress.com",
"https://web.archive.org/web/20200206215423if_/https://aliexpress.com",
"https://web.archive.org/web/20200220102855if_/https://aliexpress.com",
"https://web.archive.org/web/20200303161206if_/https://aliexpress.com",
"https://web.archive.org/web/20200310124012if_/https://aliexpress.com",
"https://web.archive.org/web/20200325145025if_/https://aliexpress.com",
"https://web.archive.org/web/20200408175553if_/https://aliexpress.com",
"https://web.archive.org/web/20200419041126if_/https://aliexpress.com",
"https://web.archive.org/web/20200430110021if_/https://aliexpress.com",
"https://web.archive.org/web/20200509095717if_/https://aliexpress.com",
"https://web.archive.org/web/20200519080637if_/https://aliexpress.com",
"https://web.archive.org/web/20200529234439if_/https://aliexpress.com",
"https://web.archive.org/web/20200610181750if_/https://aliexpress.com",
"https://web.archive.org/web/20200623102113if_/https://aliexpress.com",
"https://web.archive.org/web/20200707113900if_/https://aliexpress.com",
"https://web.archive.org/web/20200718010758if_/https://aliexpress.com",
"https://web.archive.org/web/20200727101136if_/https://aliexpress.com",
"https://web.archive.org/web/20200806035749if_/https://aliexpress.com",
"https://web.archive.org/web/20200817031426if_/https://aliexpress.com",
"https://web.archive.org/web/20200824204943if_/https://aliexpress.com",
"https://web.archive.org/web/20200906095559if_/https://aliexpress.com",
"https://web.archive.org/web/20200922082656if_/https://aliexpress.com",
"https://web.archive.org/web/20200930162019if_/https://aliexpress.com",
"https://web.archive.org/web/20201009092044if_/https://aliexpress.com",
"https://web.archive.org/web/20201017164355if_/https://aliexpress.com",
"https://web.archive.org/web/20201027131250if_/https://aliexpress.com",
"https://web.archive.org/web/20201101034450if_/https://aliexpress.com",
"https://web.archive.org/web/20201108221701if_/https://aliexpress.com",
"https://web.archive.org/web/20201115014050if_/https://aliexpress.com",
"https://web.archive.org/web/20201123162022if_/https://aliexpress.com",
"https://web.archive.org/web/20201201235538if_/https://aliexpress.com"]

def main():
    version=0
    for url in url_list:
        version += 1
        # URL to process (replace with the desired website)
        # url = "https://web.archive.org/web/20210404125451if_/https://auth.services.adobe.com/en_US/index.html?callback=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fadobeid%2Fadobedotcom2%2FAdobeID%2Ftoken%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.adobe.com%252F%2523from_ims%253Dtrue%2526old_hash%253D%2526api%253Dauthorize%26code_challenge_method%3Dplain%26use_ms_for_expiry%3Dtrue&client_id=adobedotcom2&scope=creative_cloud%2CAdobeID%2Copenid%2Cgnav%2Cread_organizations%2Cadditional_info.projectedProductContext%2Csao.ACOM_CLOUD_STORAGE%2Csao.stock%2Csao.cce_private%2Cadditional_info.roles&denied_callback=https%3A%2F%2Fims-na1.adobelogin.com%2Fims%2Fdenied%2Fadobedotcom2%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.adobe.com%252F%2523from_ims%253Dtrue%2526old_hash%253D%2526api%253Dauthorize%26response_type%3Dtoken&relay=292f24b6-8e29-4a21-84c0-db3cdf5a9695&locale=en_US&flow_type=token&idp_flow_type=login#/"
        url = "https://web.archive.org/web/20170801235720if_/https://outlook.com"
        # -------------------------------------------------------------------------
        # 2. Set up Selenium WebDriver using Chrome and webdriver-manager.
        # -------------------------------------------------------------------------
        service = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service)

        # If you wish to run headless (without opening a browser window), uncomment:
        # from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--remote-debugging-port=9223")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=service, options=chrome_options)


        # Load the target URL
        driver.get(url)
        time.sleep(3)  # Wait for the page to load (adjust as needed)

        print(f"driver loaded, page is visible..")

        js_locator_functions = read_js_file("javascript.js")


        # Inject the locator-generation code into the page
        inject_js(driver, js_locator_functions)

        # Inject and execute the widget discovery code.
        js_discover_widgets = read_js_file("discover_widgets.js")



        # Execute the discovery function and capture the results (a list of candidate objects)
        widget_candidates = driver.execute_script(js_discover_widgets)

        # Optionally print the JSON result
        print(json.dumps(widget_candidates, indent=2))

        # === STEP 3: Write out a properties file for each candidate widget ===
        # For demonstration, we write one file per candidate.
        # output_dir = "widget_properties1"
        # os.makedirs(output_dir, exist_ok=True)
        # for widget in widget_candidates:
        #     # Build a properties file content (one key=value pair per line)
        #     lines = []
        #     for key, value in widget.items():
        #         # Convert value to string, and remove newlines
        #         lines.append(f"{key}={str(value).replace(chr(10), ' ').strip()}")
        #     content = "\n".join(lines)

        #     # Use the widget_id to name the file (or any other naming convention)
        #     filename = os.path.join(output_dir, f"widget_{widget['widget_id']}.properties")
        #     with open(filename, "w", encoding="utf-8") as f:
        #         f.write(content)
        #     print(f"Wrote {filename}")


        # Create an output directory for the CSV file.
        output_dir = "outlook_widget_csv"
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

        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
