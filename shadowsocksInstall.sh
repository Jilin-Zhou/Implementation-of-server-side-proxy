#!/bin/bash

yum install -y python3 python3-pip


pip3 --version


pip3 install --upgrade pip


pip3 install shadowsocks


cat > /etc/shadowsocks.json <<EOF
{
    "server": "0.0.0.0",
    "server_port": 8388,
    "local_address": "127.0.0.1",
    "local_port": 1080,
    "password": "123456",
    "timeout": 300,
    "method": "aes-256-cfb",
    "fast_open": false
}
EOF


chmod 600 /etc/shadowsocks.json


ssserver -c /etc/shadowsocks.json -d start
# You can use the following command to turn it off yourself.
# ssserver -c /etc/shadowsocks.json -d stop


ps aux | grep ssserver
