import json
import requests

api_token = 'your_token_goes_here'
api_url_base = 'https://api.digitalocean.com/v2/'
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}


def add_ssh_key(name, filename):

    api_url = "{0}account/keys".format(api_url_base)

    with open(filename, 'r') as f:
        ssh_key = f.readline()

    ssh_key = {'name': name, 'public_key': ssh_key}

    response = requests.post(api_url, headers=headers, json=ssh_key)

    if response.status_code > 499:
        print("[!] [{0}] Server Error".format(response.status_code))
        return None
    elif response.status_code == 404:
        print("[!] [{0}] URL not found: [{1}]".format(response.status_code, api_url))
        return None
    elif response.status_code == 401:
        print("[!] [{0}] Authentication Failed".format(response.status_code))
        return None
    elif response.status_code > 399:
        print("[!] [{0}] Bad Request".format(response.status_code))
        print(ssh_key)
        print(response.content)
        return None
    elif response.status_code > 299:
        print("[!] [{0}] Unexpected redirect.".format(response.status_code))
        return None
    elif response.status_code == 201:
        added_key = json.loads(response.content)
        return added_key
    else:
        print("[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(response.status_code, response.content))
        return None

add_response = add_ssh_key('tutorial_key', '/Users/brianhogan/.ssh/sammy.pub')

if add_response is not None:
    print("Your key was added: ")
    for k, v in add_response.items():
        print('  {0}:{1}'.format(k, v))
else:
    print('[!] Request Failed')
