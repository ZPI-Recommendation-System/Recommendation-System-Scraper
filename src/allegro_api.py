import base64
import hashlib
import json
import secrets
import string
import time

import pandas as pd
import requests

from src.constants import AUTH_URL, CLIENT_ID, REDIRECT_URI, TOKEN_URL, LAPTOP_CATEGORY, CATEGORIES_URL, \
    PARTICULAR_PRODUCT_URL, PRODUCTS_URL, OUTPUT_CSV


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


def get_parameters(token, category_id=LAPTOP_CATEGORY):
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


def get_particular_product(token, category_id=LAPTOP_CATEGORY, productId=''):
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


def normalise_parameters(api_response):
    parameters_dict = dict()
    for param in api_response['parameters']:
        if param['name'] is not None:
            new_param = param['name']
            parameters_dict[new_param] = []
    return parameters_dict


def get_products(token, category_id=LAPTOP_CATEGORY, page_id=''):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        params = {
            "category.id": category_id,
            "phrase": "laptop",
            "page.id": page_id
        }
        products_result = requests.get(PRODUCTS_URL, headers=headers, params=params, verify=False)
        return json.loads(products_result.text)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_all_products(access_token, category_id=LAPTOP_CATEGORY):
    all_products = []
    products_response = get_products(access_token, category_id)
    if products_response['products'] is not None:
        products = products_response['products']
        all_products.append(products)
    page_id = get_next_page(products_response)
    while page_id is not None:
        products_response = get_products(access_token, category_id, page_id)
        if 'products' in products_response and products_response['products'] is not None:
            products = products_response['products']
            all_products.append(products)
        page_id = get_next_page(products_response)
    return all_products


def normalise_products(access_token, products_pages, parameters):
    data = dict()
    data['ID'] = []
    data['Name'] = []
    data['Zdjęcia'] = []

    for parameter in parameters:
        data[parameter] = []

    for page in products_pages:
        for product in page:
            data['ID'].append(product['id'])
            data['Name'].append(product['name'])
            data['Zdjęcia'].append(str(list(map(lambda image: image['url'], product['images']))))

            null_columns = list(parameters.keys())
            if product['parameters'] is not None:
                product_parameters = product['parameters']
                for product_parameter in product_parameters:
                    param = product_parameter['name']
                    if param in data:
                        null_columns.remove(param)
                        data[param].append(str(product_parameter['valuesLabels']))
                for column in null_columns:
                    data[column].append(None)
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


def dump_to_csv(data):
    pd.DataFrame(data).to_csv(OUTPUT_CSV, header=True, index=False)


def scrape():
    code_verifier = generate_code_verifier()
    authorization_code = get_authorization_code(code_verifier)
    response = get_access_token(authorization_code, code_verifier)
    access_token = response['access_token']
    print(f"access token = {access_token}")
    parameters = normalise_parameters(get_parameters(access_token, LAPTOP_CATEGORY))
    products = get_all_products(access_token, LAPTOP_CATEGORY)
    data = normalise_products(access_token, products, parameters)
    dump_to_csv(data)
    return data


if __name__ == "__main__":
    start = time.time()
    scrape()
    end = time.time()
    print("Run time: " + str(int((int(end - start) / 60))) + " minutes")
