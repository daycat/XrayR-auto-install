# XrayR-auto-install
A simple script to install XrayR and configure Vmess+ WS + TLS

## Setup

```sh
pip3 install -r requirements.txt
```

## Usage:

```sh
python3 main.py
```

## Configuration:

```yaml
Cloudflare:
  Email: [your cloudflare email]
  API: [your cloudflare global api key]
  Zone: [your domain zone id]
  Domain: [your domain / subdomain]
  Gen: true

Nodes:
  API: [your panel url]
  Token: [your panel token]
  Panel: [your panel type]
```

## Thanks
[MaxMind](https://www.maxmind.com/en/home) for providing a free GeoIP database       
[XrayR](https://github.com/Misaka-blog/XrayR) for installation script        

## Contact me
[Telegram](https://t.me/day_cat)

