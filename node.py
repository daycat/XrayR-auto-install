import paramiko as pm

def install(IP, Password, Domain, webapi, token, email, nodeID, panel):
    client = pm.client.SSHClient()
    client.set_missing_host_key_policy(pm.AutoAddPolicy())
    client.connect(IP, username='root', password=Password)

    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('''
apt update 
apt install wget -y''')
    print(ssh_stdout.read())
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('''
wget -N https://raw.githubusercontent.com/XrayR-project/XrayR-release/master/install.sh && bash install.sh
''')
    print(ssh_stdout.read())
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('''
curl https://get.acme.sh | sh -s email=''' + email + '''
/root/.acme.sh/acme.sh --issue --standalone -d ''' + Domain + '''
systectl stop XrayR
rm -fr /etc/XrayR/config.yml
''')
    print(ssh_stdout.read())
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('''
cat <<EOF > /etc/XrayR/config.yml
Log:
  Level: info # Log level: none, error, warning, info, debug 
  AccessPath: # /etc/XrayR/access.Log
  ErrorPath: # /etc/XrayR/error.log
DnsConfigPath: # /etc/XrayR/dns.json # Path to dns config, check https://xtls.github.io/config/dns.html for help
RouteConfigPath: # /etc/XrayR/route.json # Path to route config, check https://xtls.github.io/config/routing.html for help
InboundConfigPath: # /etc/XrayR/custom_inbound.json # Path to custom inbound config, check https://xtls.github.io/config/inbound.html for help
OutboundConfigPath: # /etc/XrayR/custom_outbound.json # Path to custom outbound config, check https://xtls.github.io/config/outbound.html for help
ConnetionConfig:
  Handshake: 4 # Handshake time limit, Second
  ConnIdle: 30 # Connection idle time limit, Second
  UplinkOnly: 2 # Time limit when the connection downstream is closed, Second
  DownlinkOnly: 4 # Time limit when the connection is closed after the uplink is closed, Second
  BufferSize: 64 # The internal cache size of each connection, kB 
Nodes:
  -
    PanelType: "'''+panel+'''" # Panel type: SSpanel, V2board, PMpanel, Proxypanel
    ApiConfig:
      ApiHost: "'''+webapi+'''"
      ApiKey: "'''+token+'''"
      NodeID: '''+nodeID+'''
      NodeType: V2ray # Node type: V2ray, Shadowsocks, Trojan, Shadowsocks-Plugin
      Timeout: 30 # Timeout for the api request
      EnableVless: false # Enable Vless for V2ray Type
      EnableXTLS: false # Enable XTLS for V2ray and Trojan
      SpeedLimit: 0 # Mbps, Local settings will replace remote settings, 0 means disable
      DeviceLimit: 0 # Local settings will replace remote settings, 0 means disable
      RuleListPath: # /etc/XrayR/rulelist Path to local rulelist file
    ControllerConfig:
      ListenIP: 0.0.0.0 # IP address you want to listen
      SendIP: 0.0.0.0 # IP address you want to send pacakage
      UpdatePeriodic: 60 # Time to update the nodeinfo, how many sec.
      EnableDNS: false # Use custom DNS config, Please ensure that you set the dns.json well
      DNSType: AsIs # AsIs, UseIP, UseIPv4, UseIPv6, DNS strategy
      EnableProxyProtocol: false # Only works for WebSocket and TCP
      EnableFallback: false # Only support for Trojan and Vless
      FallBackConfigs:  # Support multiple fallbacks
        -
          SNI: # TLS SNI(Server Name Indication), Empty for any
          Alpn: # Alpn, Empty for any
          Path: # HTTP PATH, Empty for any
          Dest: 80 # Required, Destination of fallback, check https://xtls.github.io/config/features/fallback.html for details.
          ProxyProtocolVer: 0 # Send PROXY protocol version, 0 for dsable
      CertConfig:
        CertMode: file # Option about how to get certificate: none, file, http, dns. Choose "none" will forcedly disable the tls config.
        CertDomain: "'''+Domain+'''" # Domain to cert
        CertFile: /root/.acme.sh/'''+Domain+'''/fullchain.cer
        KeyFile: /root/.acme.sh/'''+Domain+'/'+Domain+'''.key        
        Provider: alidns # DNS cert provider, Get the full support list here: https://go-acme.github.io/lego/dns/
        Email: test@me.com
        DNSEnv: # DNS ENV option used by DNS provider
          ALICLOUD_ACCESS_KEY: aaa
          ALICLOUD_SECRET_KEY: bbb
EOF
    ''')
    print(ssh_stdout.read())
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('''
systemctl start XrayR
systemctl enable XrayR
''')

    print(ssh_stdout.read())
