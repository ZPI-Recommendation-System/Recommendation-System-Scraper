from pprint import pprint

import requests
import json
import time

CLIENT_ID = ""          # wprowadź Client_ID aplikacji
CLIENT_SECRET = ""      # wprowadź Client_Secret aplikacji
CODE_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/device"
TOKEN_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/token"
OFFER_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/offers/7693390861"

def get_code():
    try:
        payload = {'client_id': CLIENT_ID}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        api_call_response = requests.post(CODE_URL, auth=(CLIENT_ID, CLIENT_SECRET),
                                          headers=headers, data=payload, verify=False)
        return api_call_response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_access_token(device_code):
    try:
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'urn:ietf:params:oauth:grant-type:device_code', 'device_code': device_code}
        api_call_response = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET),
                                          headers=headers, data=data, verify=False)
        return api_call_response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def await_for_access_token(interval, device_code):
    while True:
        time.sleep(interval)
        result_access_token = get_access_token(device_code)
        token = json.loads(result_access_token.text)
        if result_access_token.status_code == 400:
            if token['error'] == 'slow_down':
                interval += interval
            if token['error'] == 'access_denied':
                break
        else:
            return token['access_token']

def get_products(token):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json", 'Content-type': "application/vnd.allegro.public.v1+json"}
        products_result = requests.get(OFFER_URL, headers=headers, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def main():
    code = get_code()
    result = json.loads(code.text)
    pprint(result)
    print("User, open this address in the browser:" + result['verification_uri_complete'])
    access_token = await_for_access_token(int(result['interval']), result['device_code'])
    print("access_token = " + access_token)
    print(get_products(access_token))


if __name__ == "__main__":
    main()