from yaml.loader import SafeLoader
from node import install
from cloudflare import resolve
import string
import maxminddb
import yaml
import random

if __name__ == '__main__':
    with open('config.yaml', 'r') as reader:
        config = yaml.safe_load(reader)

    config['Nodes']['IP'] = input("IP: ")
    config['Nodes']['Password'] = input("Password: ")
    try:
        with maxminddb.open_database('GeoLite2-Country.mmdb') as reader:
            country = reader.get(config['Nodes']['IP'])['country']['iso_code']
            zhCN_country = reader.get(config['Nodes']['IP'])['country']['names']['zh-CN']
    except TypeError:
        country = input("Failed to get IP country. Please update MMDB file.\nPlease insert country of IP manually here: ")

    domain = country+ '-'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3))+'.'+config['Cloudflare']['Domain']
    print('Adding DNS records...')
    resolve(domain, config['Nodes']['IP'], config['Cloudflare']['Email'], config['Cloudflare']['API'], config['Cloudflare']['Zone'])
    print('Success')
    print('Domain: '+domain)
    print('Country: '+country)
    config['Nodes']['NodeID'] = input('Now head to panel and add this node. Input your node ID here: ')
    install(config['Nodes']['IP'], config['Nodes']['Password'], domain, config['Nodes']['API'], config['Nodes']['Token'], config['Cloudflare']['Email'], config['Nodes']['NodeID'], config['Nodes']['Panel'])





