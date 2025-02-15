import requests
import numpy as np
import pandas as pd
import time
# Define base and end archived URLs
OLD_WEB_SITES = {
    "adobe": "https://web.archive.org/web/20180702000525if_/https://www.adobe.com/",
    "aliexpress": "https://web.archive.org/web/20170401212838if_/https://www.aliexpress.com/",
    "amazon": "https://web.archive.org/web/20180101000000if_/https://www.amazon.com/",
    "apple": "https://web.archive.org/web/20171002003641if_/https://www.apple.com/",
    "bestbuy": "https://web.archive.org/web/20180401if_/https://www.bestbuy.com/",
    "bing": "https://web.archive.org/web/20191201234246if_/http://www.bing.com/",
    "chase": "https://web.archive.org/web/20181202045722if_/https://www.chase.com/",
    "cnn": "https://web.archive.org/web/20180402002511if_/https://www.cnn.com/",
    "craigslist": "https://web.archive.org/web/20160331202313if_/http://sfbay.craigslist.org/",
    "dropbox": "https://web.archive.org/web/20191202001310if_/https://www.dropbox.com/?landing=dbv2",
    "ebay": "https://web.archive.org/web/20180601235610if_/https://www.ebay.com/",
    "espn": "https://web.archive.org/web/20191201233248if_/https://www.espn.com/",
    "etsy": "https://web.archive.org/web/20191002005309if_/https://www.etsy.com/",
    "facebook": "https://web.archive.org/web/20161101030329/https://www.facebook.com/",
    "fidelity": "https://web.archive.org/web/20180102000534if_/https://www.fidelity.com/",
    "salesforce": "https://web.archive.org/web/20190201214503if_/https://www.salesforce.com/products/platform/products/force/?d=70130000000f27V&internal=true",
    "foxnews": "https://web.archive.org/web/20180801233843if_/http://www.foxnews.com/",
    "google": "https://web.archive.org/web/20180802000242if_/https://www.google.com/",
    "hulu": "https://web.archive.org/web/20191201225319if_/https://www.hulu.com/welcome",
    "imdb": "https://web.archive.org/web/20190602000208if_/https://www.imdb.com/",
    "indeed": "https://web.archive.org/web/20151202004335if_/http://www.indeed.com/",
    "instagram": "https://web.archive.org/web/20180602003550if_/https://www.instagram.com/",
    "instructure": "https://web.archive.org/web/20171101205846if_/https://www.instructure.com/",
    "intuit": "https://web.archive.org/web/20190401223517if_/https://www.intuit.com/",
    "linkedin": "https://web.archive.org/web/20170802004444if_/https://www.linkedin.com/",
    "outlook": "https://web.archive.org/web/20170801235424if_/https://outlook.live.com/owa/",
    "microsoft": "https://web.archive.org/web/20160602021830if_/http://www.microsoft.com/en-us/",
    "shopify": "https://web.archive.org/web/201802if_/https://login.microsoftonline.com/",
    "netflix": "https://web.archive.org/web/20160101232822if_/https://www.netflix.com/ca/",
    "nytimes": "https://web.archive.org/web/20181201235804if_/https://www.nytimes.com/",
    "office": "https://web.archive.org/web/20190301225930if_/https://www.office.com/",
    "okta": "https://web.archive.org/web/20171102031615if_/https://www.okta.com/",
    "paypal": "https://web.archive.org/web/20170304235734if_/https://www.paypal.com/us/home",
    "reddit": "https://web.archive.org/web/20171001232623if_/https://www.reddit.com/",
    "spotify": "https://web.archive.org/web/20170602003201if_/https://www.spotify.com/us/",
    "target": "https://web.archive.org/web/20170702000250if_/https://www.target.com/",
    "twitch": "https://web.archive.org/web/20160301234356if_/http://www.twitch.tv/",
    "twitter": "https://web.archive.org/web/20170702000250if_/https://twitter.com/",
    "ups": "https://web.archive.org/web/20170629135919if_/https://www.ups.com/us/en/Home.page",
    "usps": "https://web.archive.org/web/20171202144652/https://www.usps.com/",
    "walmart": "https://web.archive.org/web/20170902000248if_/https://www.walmart.com/",
    "wellsfargo": "https://web.archive.org/web/20191002055021if_/https://www.wellsfargo.com/",
    "wikipedia": "https://web.archive.org/web/20170901235350if_/https://www.wikipedia.org/",
    "yahoo": "https://web.archive.org/web/20181101/https://www.yahoo.com/",
    "youtube": "https://web.archive.org/web/20190801/https://www.youtube.com/",
    "zillow": "https://web.archive.org/web/20170602000250if_/https://www.zillow.com/",
    "zoom": "https://web.archive.org/web/20160501084828/http://zoom.us/"
}

NEW_WEB_SITES = {
    "adobe": "https://web.archive.org/web/20201102003024if_/https://www.adobe.com/",
    "aliexpress": "https://web.archive.org/web/20201201235538if_/https://www.aliexpress.com/",
    "amazon": "https://web.archive.org/web/20201201if_/https://www.amazon.com/",
    "apple": "https://web.archive.org/web/20201201235612if_/https://www.apple.com/",
    "bestbuy": "https://web.archive.org/web/20201201233637if_/https://www.bestbuy.com/",
    "bing": "https://web.archive.org/web/20201201234246if_/http://www.bing.com/",
    "chase": "https://web.archive.org/web/20201202004756if_/https://www.chase.com/",
    "cnn": "https://web.archive.org/web/20201201235755if_/https://www.cnn.com/",
    "craigslist": "https://web.archive.org/web/20201204000601if_/https://sfbay.craigslist.org/",
    "dropbox": "https://web.archive.org/web/20201202001310if_/https://www.dropbox.com/?landing=dbv2",
    "ebay": "https://web.archive.org/web/20201202000703if_/https://www.ebay.com/",
    "espn": "https://web.archive.org/web/20201201233248if_/https://www.espn.com/",
    "etsy": "https://web.archive.org/web/20201201233425if_/https://www.etsy.com/",
    "facebook": "https://web.archive.org/web/20201201011205/https://www.facebook.com/",
    "fidelity": "https://web.archive.org/web/20201201211643if_/https://www.fidelity.com/",
    "salesforce": "https://web.archive.org/web/20201201203858if_/https://www.salesforce.com/products/platform/products/force/?sfdc-redirect=300&bc=WA",
    "foxnews": "https://web.archive.org/web/20201201235925if_/https://www.foxnews.com/",
    "google": "https://web.archive.org/web/20201201235949if_/https://www.google.com/",
    "hulu": "https://web.archive.org/web/20201202000152if_/https://www.hulu.com/welcome",
    "imdb": "https://web.archive.org/web/20201201233544if_/https://www.imdb.com/",
    "indeed": "https://web.archive.org/web/20201201225703if_/https://www.indeed.com/",
    "instagram": "https://web.archive.org/web/20201202000011if_/https://www.instagram.com/",
    "instructure": "https://web.archive.org/web/20201202000839if_/https://www.instructure.com/",
    "intuit": "https://web.archive.org/web/20201202032948if_/https://www.intuit.com/",
    "linkedin": "https://web.archive.org/web/20201202011337if_/https://www.linkedin.com/",
    "outlook": "https://web.archive.org/web/20201201235603if_/https://outlook.live.com/owa/",
    "microsoft": "https://web.archive.org/web/20201201if_/https://login.microsoftonline.com/",
    "shopify": "https://web.archive.org/web/20201202023130if_/http://myshopify.com/",
    "netflix": "https://web.archive.org/web/20201201180555if_/https://www.netflix.com/",
    "nytimes": "https://web.archive.org/web/20201201232252if_/https://www.nytimes.com/",
    "office": "https://web.archive.org/web/20201201231944if_/https://www.office.com/",
    "okta": "https://web.archive.org/web/20201202011337if_/https://www.okta.com/",
    "paypal": "https://web.archive.org/web/20201202030231if_/https://www.paypal.com/us/home",
    "reddit": "https://web.archive.org/web/20201201225657if_/https://www.reddit.com/",
    "spotify": "https://web.archive.org/web/20201202000137if_/https://www.spotify.com/us/",
    "target": "https://web.archive.org/web/20201201223651if_/https://www.target.com/",
    "twitch": "https://web.archive.org/web/20201201233100if_/http://www.twitch.tv/",
    "twitter": "https://web.archive.org/web/20201201231150if_/https://twitter.com/",
    "ups": "https://web.archive.org/web/20201201093221if_/https://www.ups.com/us/en/Home.page",
    "usps": "https://web.archive.org/web/20201202032259if_/https://www.usps.com/",
    "walmart": "https://web.archive.org/web/20201201005312if_/https://www.walmart.com/",
    "wellsfargo": "https://web.archive.org/web/20201201230245if_/https://www.wellsfargo.com/",
    "wikipedia": "https://web.archive.org/web/20201201231741if_/https://www.wikipedia.org/",
    "yahoo": "https://web.archive.org/web/20201201235645if_/https://www.yahoo.com/",
    "youtube": "https://web.archive.org/web/20201201225204if_/https://www.youtube.com/",
    "zillow": "https://web.archive.org/web/20201201200428if_/https://www.zillow.com/",
    "zoom": "https://web.archive.org/web/20201201232123if_/https://www.zoom.us/"
}


# Extract timestamp from archive URL
def extract_timestamp(url):
    return url.split("/web/")[1].split("if_")[0][:14]

# Get 100 archived snapshots within the given range with retries
def get_archived_snapshots(domain, start_ts, end_ts, limit=100, retries=3):
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}&output=json"
    print(f"URL: {url}")

    for attempt in range(retries):
        print(f"attempt number: {attempt}")
        try:
            response = requests.get(url, timeout=10)  # Adding a timeout to avoid hanging indefinitely

            if response.status_code != 200:
                print(f"⚠️ Failed to fetch snapshots for {domain} (attempt {attempt + 1})")
                continue
            print("I'm not stuck at request/response")
            snapshots = response.json()[1:]  # Ignore the header row
            timestamps = [snap[1] for snap in snapshots]  # Extract timestamps
            print(timestamps)
            # Filter timestamps within range
            filtered_timestamps = [ts for ts in timestamps if start_ts <= ts <= end_ts]

            # Select exactly 100 timestamps
            if len(filtered_timestamps) >= limit:
                indices = np.linspace(0, len(filtered_timestamps) - 1, limit, dtype=int)
                selected_timestamps = [filtered_timestamps[i] for i in indices]
            else:
                selected_timestamps = filtered_timestamps  # Use all available timestamps

            return selected_timestamps

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching snapshots for {domain}: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(5)  # Wait before retrying
            else:
                print("Max retries reached. Skipping this domain.")

    return []

# Process each website
for site, old_url in OLD_WEB_SITES.items():
    new_url = NEW_WEB_SITES.get(site)
    if not new_url:
        continue

    # Extract timestamps
    old_timestamp = extract_timestamp(old_url)
    new_timestamp = extract_timestamp(new_url)

    # Fetch 100 snapshots
    timestamps = get_archived_snapshots(site + ".com", old_timestamp, new_timestamp)

    if not timestamps:
        print(f"⚠️ No snapshots found for {site}. Skipping...")
        continue

    # Construct archived URLs
    archived_urls = [f"https://web.archive.org/web/{ts}/https://{site}.com" for ts in timestamps]

    # Store results in a separate CSV file for each website
    results = [[site, ts, url] for ts, url in zip(timestamps, archived_urls)]
    df = pd.DataFrame(results, columns=["Website", "Timestamp", "Archived URL"])
    df.to_csv(f"{site}_archived_versions.csv", index=False)

    print(f"Data saved to {site}_archived_versions.csv")
