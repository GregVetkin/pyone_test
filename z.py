import base64
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




def make_https_request(url, username, password, session_dir, verify_ssl=False):
    try:
        auth_string = f"{username}:{password}"
        encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
        headers = {
           "Authorization": f"Basic {encoded_auth}",
           "Cookie": f"rack.session={session_dir}"
        }
        response = requests.get(url, headers=headers, verify=verify_ssl)
        response.raise_for_status()
        return response
    
    except requests.exceptions.RequestException as e:
        print(f"Exception raised: {e}")
        pass
    

url = "https://10.0.70.20/brestcloud/one-apache2.cgi"
username = "brestadm"
password = "Qwe!2345"
session_dir = "Af86dec360df74c68775cb14660df3a4086e3615b854d2883172d5096923a5f34"



while True:
    start = time.perf_counter()
    make_https_request(url, username, password, session_dir)
    print(time.perf_counter() - start)