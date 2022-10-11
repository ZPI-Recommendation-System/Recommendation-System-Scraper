from pprint import pprint
import base64
import hashlib
import secrets
import string

import requests
import json

CLIENT_ID = "57fa927c1f0b426b9419be5de3874bfa"          # wprowadź Client_ID aplikacji
CLIENT_SECRET = "tNlus0WGLDa52dLwSAnkmOgTCuVCp8Bz9Y9DdUjBUyuj5TJKhGqX92Hk3mIK4iyZ"      # wprowadź Client_Secret aplikacji
REDIRECT_URI = "http://localhost:8000"       # wprowadź redirect_uri
AUTH_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize"
TOKEN_URL = "https://allegro.pl.allegrosandbox.pl/auth/oauth/token"
PRODUCTS_URL = "https://api.allegro.pl.allegrosandbox.pl/sale/products"


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


def get_products(token, category_id='491', page_id=''):
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


def get_next_page(products):
    if products['nextPage'] is not None:
        if products['nextPage']['id'] is not None:
            return products['nextPage']['id']
    return None


def main():
    code_verifier = generate_code_verifier()
    authorization_code = get_authorization_code(code_verifier)
    response = get_access_token(authorization_code, code_verifier)
    access_token = response['access_token']
    print(f"access token = {access_token}")
    products = get_products(access_token, '491')
    pprint(products)
    page_id = get_next_page(products)
    while page_id is not None:
        products = get_products(access_token, '491', page_id)
        pprint(products)
        page_id = get_next_page(products)


if __name__ == "__main__":
    main()
