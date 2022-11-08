import base64
import hashlib
import json
import secrets
import string
from pprint import pprint

import pandas as pd
import requests

CLIENT_ID = "b8a9a702550e42f0a12ad3eb524531c0"  # wprowadź Client_ID aplikacji
CLIENT_SECRET = "uKGWlKVj5akLa0ZyVnSCcrUmLMfmhFL9BJ0Usi4KKuVUAqa6f0eo0nQ1eC5LFpDy"  # wprowadź Client_Secret aplikacji
REDIRECT_URI = "http://localhost:8000"  # wprowadź redirect_uri
AUTH_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize"
TOKEN_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/token"
PRODUCTS_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/products"
ALL_CATEGORIES_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/categories"
OFFER_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/offers/{offerId}"
OFFERS_URL = "https://api.allegro.pl.allegrosandbox.pl/offers/listing"
CATEGORIES_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/categories/{categoryId}/parameters"
PARTICULAR_PRODUCT_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/products/{productId}"
LAPTOP_CATEGORY = '491'

def generate_code_verifier():
    code_verifier = ''.join((secrets.choice(string.ascii_letters) for i in range(40)))
    return code_verifier


def generate_code_challenge(code_verifier):
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    base64_encoded = base64.urlsafe_b64encode(hashed).decode('utf-8')
    code_challenge = base64_encoded.replace('=', '')
    return code_challenge


def get_authorization_code(code_verifier):
    code_challenge = generate_code_challenge(code_verifier)
    authorization_redirect_url = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}" \
                                 f"&code_challenge_method=S256&code_challenge={code_challenge}"
    print("Zaloguj do Allegro - skorzystaj z url w swojej przeglądarce oraz wprowadź authorization code ze zwróconego "
          "url: ")
    print(f"--- {authorization_redirect_url} ---")
    authorization_code = input('code: ')
    return authorization_code


def get_access_token(authorization_code, code_verifier):
    try:
        data = {'grant_type': 'authorization_code', 'code': authorization_code,
                'redirect_uri': REDIRECT_URI, 'code_verifier': code_verifier}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False, allow_redirects=False)
        response_body = json.loads(access_token_response.text)
        return response_body
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_category_parameters(token, category_id=LAPTOP_CATEGORY):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        params = {
            "category.id": category_id,
            "phrase": "laptop",
        }
        products_result = requests.get(CATEGORIES_URL.replace("{categoryId}", category_id), headers=headers,
                                       params=params, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_categories(token):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        products_result = requests.get(ALL_CATEGORIES_URL, headers=headers, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_offer(token, category_id=LAPTOP_CATEGORY, offerId=''):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        params = {
            "category.id": category_id,
            "phrase": "laptop",
        }
        products_result = requests.get(OFFER_URL.replace("{offerId}", offerId), headers=headers,
                                       params=params, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_offers(token, category_id=LAPTOP_CATEGORY):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        params = {
            "category.id": category_id,
            "phrase": "laptop",
            "parameter.11323": "11323_1"
        }
        products_result = requests.get(OFFERS_URL, headers=headers, params=params, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_items_from_offers(offers):
    items = dict()
    if offers['items'] is not None:
        pass


def get_product_by_id(token, category_id=LAPTOP_CATEGORY, productId=''):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        params = {
            "category.id": category_id,
            "phrase": "laptop",
        }
        products_result = requests.get(PARTICULAR_PRODUCT_URL.replace("{productId}", productId), headers=headers,
                                       params=params, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def create_params_dict(api_response):
    parameters_dict = dict()
    for param in api_response['parameters']:
        if param['name'] is not None:
            new_param = param['name']
            parameters_dict[new_param] = []
    return parameters_dict


def get_products_page(token, category_id=LAPTOP_CATEGORY, page_id=''):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        params = {
            "category.id": category_id,
            "phrase": "laptopy",
            "page.id": page_id
        }
        products_result = requests.get(PRODUCTS_URL, headers=headers, params=params, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_all_products(access_token, category_id=LAPTOP_CATEGORY):
    products_pages = []
    products_response = get_products_page(access_token, category_id)
    if products_response['products'] is not None:
        products = products_response['products']
        products_pages.append(products)
    page_id = get_next_page(products_response)
    while page_id is not None:
        products_response = get_products_page(access_token, category_id, page_id)
        if products_response['products'] is not None:
            products = products_response['products']
            products_pages.append(products)
        page_id = get_next_page(products_response)
    return products_pages


def normalise_products(access_token, products_pages, parameters):
    data = dict()

    data['ID'] = []
    data['Name'] = []
    for parameter in parameters:
        data[parameter] = []
    for page in products_pages:
        for product in page:
            data['ID'].append(product['id'])
            data['Name'].append(product['name'])

            pprint(get_product_by_id(access_token, LAPTOP_CATEGORY, product['id']))
            null_collumns = list(parameters.keys())
            if product['parameters'] is not None:
                product_parameters = product['parameters']
                for product_parameter in product_parameters:
                    param = product_parameter['name']
                    if param in data:
                        null_collumns.remove(param)
                        data[param].append(str(product_parameter['valuesLabels']))
                for collumn in null_collumns:
                    data[collumn].append(None)
    return data


def print_product_console(data):
    index = 0
    max_len = len(data['ID'])
    while index < max_len:
        row_string = ""
        for param in data:
            if data[param][index] is None:
                row_string += "-"
            else:
                row_string += data[param][index]
            row_string += ("\t" * 10)
        print(row_string)
        index += 1


def get_next_page(products):
    if products['nextPage'] is not None:
        if products['nextPage']['id'] is not None:
            return products['nextPage']['id']
    return None


def dump_to_xlsx(data):
    pd.DataFrame(data).to_excel("laptops.xlsx", encoding='utf-8', index=False)


def main():
    code_verifier = generate_code_verifier()
    authorization_code = get_authorization_code(code_verifier)
    response = get_access_token(authorization_code, code_verifier)
    access_token = response['access_token']
    print(f"access token = {access_token}")
    # pprint(get_offers(access_token, LAPTOP_CATEGORY))
    parameters = create_params_dict(get_category_parameters(access_token, LAPTOP_CATEGORY))
    products = get_all_products(access_token, LAPTOP_CATEGORY)
    data = normalise_products(access_token, products, parameters)
    print_product_console(data)
    dump_to_xlsx(data)

if __name__ == "__main__":
    main()
