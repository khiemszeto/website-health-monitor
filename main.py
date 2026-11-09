from urllib import request
from urllib.error import URLError, HTTPError
from datetime import datetime
import sys

path_to_file = sys.argv[1]
is_a_web_failed = False
network_probe = "http://captive.apple.com"

with open("websites_health.log", "a") as log:
    # check_at format: DD-MM-YYYY HH:MM:SS
    checked_at = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    # check the network connection and exit with code 2 if no network connection
    try:
        with request.urlopen(network_probe, timeout=5) as response:
            pass
    except HTTPError:
        pass
    except URLError as error:
        log.write(f"NO NETWORK CONNECTION: {checked_at} {error.reason}\n")
        print(f"NO NETWORK CONNECTION: {error.reason}")
        sys.exit(2)
    
    # check the websites health
    with open(path_to_file, 'r') as file:
        for line in file:
            url = line.strip()
            if url == "":
                continue

            # update the checked_at time
            checked_at = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

            try:
                with request.urlopen(url, timeout=10) as response:
                    log.write(f"OK: {url} {checked_at}\n")
                    print(f"OK: {url} returned {response.status}")
            except HTTPError as error:
                log.write(f"HTTP Error: {url} {checked_at} {error.code}\n")
                print(f"HTTP Error: {error.code}")
                is_a_web_failed = True
            except URLError as error:
                log.write(f"URL Error: {url} {checked_at} {error.reason}\n")
                print(f"URL Error: {error.reason}")
                is_a_web_failed = True

# exit with code 1 if any website is failed
if is_a_web_failed:
    sys.exit(1)