import json
import time

import pandas as pd
import requests

from src.constants import CLIENT_ID, TOKEN_URL, LAPTOP_CATEGORY, CATEGORIES_URL, \
    PARTICULAR_PRODUCT_URL, PRODUCTS_URL, OUTPUT_CSV, CODE_URL, CLIENT_SECRET


def get_code():
    try:
        payload = {'client_id': CLIENT_ID}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        api_call_response = requests.post(CODE_URL, auth=(CLIENT_ID, CLIENT_SECRET),
                                          headers=headers, data=payload)
        return api_call_response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_access_token(device_code):
    try:
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'urn:ietf:params:oauth:grant-type:device_code', 'device_code': device_code}
        api_call_response = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET),
                                          headers=headers, data=data)
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


def get_parameters(token, category_id=LAPTOP_CATEGORY):
    try:
        headers = {'Authorization': 'Bearer ' + token, 'Accept': "application/vnd.allegro.public.v1+json"}
        params = {
            "category.id": category_id,
            "phrase": "laptop",
        }
        products_result = requests.get(CATEGORIES_URL.replace("{categoryId}", category_id), headers=headers,
                                       params=params)
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
                                       params=params)
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
        products_result = requests.get(PRODUCTS_URL, headers=headers, params=params)
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
    data.to_csv(OUTPUT_CSV, header=True, index=False)


def scrape():
    code = get_code()
    result = json.loads(code.text)
    print("User, open this address in the browser:" + result['verification_uri_complete'])
    access_token = await_for_access_token(int(result['interval']), result['device_code'])
    print(f"access token = {access_token}")
    parameters = normalise_parameters(get_parameters(access_token, LAPTOP_CATEGORY))
    products = get_all_products(access_token, LAPTOP_CATEGORY)
    data = normalise_products(access_token, products, parameters)
    data = pd.DataFrame(data)
    dump_to_csv(data)
    return data


if __name__ == "__main__":
    start = time.time()
    scrape()
    end = time.time()
    print("Run time: " + str(int((int(end - start) / 60))) + " minutes")
