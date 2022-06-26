import requests
import json

def resolve(domain, ip, email, api, zone):
    cloudflare_headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': api,
    }
    cfjson = {
        'type': 'A',
        'name': domain,
        'content': ip,
        'ttl': 60,
        'priority': 10,
        'proxied': False,
    }
    response = json.loads(requests.post(url='https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records', headers=cloudflare_headers, json=cfjson).text)
    if response['success'] == True:
        return 0
    else:
        exit(1)