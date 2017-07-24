import json
import requests

api_token = 'your_token_goes_here'
api_url_base = 'https://api.digitalocean.com/v2/'
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}


def get_ssh_keys():

    api_url = "{0}account/keys".format(api_url_base)

    response = requests.get(api_url, headers=headers)

    if response.status_code >= 500:
        print("[!] [{0}] Server Error".format(response.status_code))
        return None
    elif response.status_code == 404:
        print("[!] [{0}] URL not found: [{1}]".format(response.status_code, api_url))
        return None
    elif response.status_code == 401:
        print("[!] [{0}] Authentication Failed".format(response.status_code))
        return None
    elif response.status_code == 400:
        print("[!] [{0}] Bad Request".format(response.status_code))
        return None
    elif response.status_code >= 300:
        print("[!] [{0}] Unexpected Redirect".format(response.status_code))
        return None
    elif response.status_code == 200:
        ssh_keys = json.loads(response.content.decode('utf-8'))
        return ssh_keys
    else:
        print("[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(response.status_code, response.content))
    return None

ssh_keys = get_ssh_keys()

if ssh_keys is not None:
    print("Here are your keys: ")
    for key, details in enumerate(ssh_keys['ssh_keys']):
        print("Key {}:".format(key))
        for k, v in details.items():
            print('  {0}:{1}'.format(k, v))
else:
    print('[!] Request Failed')
