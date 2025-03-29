```md
# Shadowsocks Server Installation Guide

## 1. Server Requirements
- **Operating System**: CentOS 7
- **Network Access**: The server must be able to access GitHub and required software repositories
- **Permissions**: Root or sudo privileges are required

---

## 2. Download and Execute the Installation Script
You can use `wget` or `curl` to download and execute `shadowsocksInstall.sh`.

### **Method 1: Download and Execute Manually**
```bash
# Switch to root user (optional)
sudo -i  

# Download the installation script
wget -O shadowsocksInstall.sh https://raw.githubusercontent.com/Jilin-Zhou/Implementation-of-server-side-proxy/main/shadowsocksInstall.sh

# Grant execute permission
chmod +x shadowsocksInstall.sh  

# Run the script
./shadowsocksInstall.sh
```

### **Method 2: One-Command Execution**
To download and execute the script in one step, use:
```bash
bash <(curl -s https://raw.githubusercontent.com/Jilin-Zhou/Implementation-of-server-side-proxy/main/shadowsocksInstall.sh)
```
or:
```bash
bash <(wget -qO- https://raw.githubusercontent.com/Jilin-Zhou/Implementation-of-server-side-proxy/main/shadowsocksInstall.sh)
```

---

## 3. Firewall Configuration (Optional)
If `firewalld` is enabled on your server, you need to allow Shadowsocks' listening port (default `8388`):
```bash
firewall-cmd --permanent --add-port=8388/tcp  
firewall-cmd --permanent --add-port=8388/udp  
firewall-cmd --reload
```

---

## 4. Shadowsocks Configuration File
The script automatically generates the configuration file at `/etc/shadowsocks.json` with the following default settings:
```json
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
```
To modify the configuration, edit the file:
```bash
vim /etc/shadowsocks.json
```
After making changes, restart Shadowsocks to apply the new settings.

---

## 5. Start & Manage Shadowsocks
### **Start Shadowsocks Server**
```bash
ssserver -c /etc/shadowsocks.json -d start
```
### **Stop Shadowsocks Server**
```bash
ssserver -c /etc/shadowsocks.json -d stop
```
### **Restart Shadowsocks**
```bash
ssserver -c /etc/shadowsocks.json -d restart
```

---

## 6. Verify Shadowsocks is Running
```bash
ps aux | grep ssserver
```
or:
```bash
netstat -plntu | grep 8388
```
If you see the `ssserver` process running, Shadowsocks is successfully set up.

---

## 7. Client Configuration
Install Shadowsocks on your local client (Windows, macOS, Android) and configure it with the following settings:
- **Server Address**: Your server's public IP
- **Port**: 8388
- **Password**: 123456
- **Encryption Method**: aes-256-cfb

---

## 8. Troubleshooting
### **1. Shadowsocks Won't Start?**
- Check if it's already running:
  ```bash
  ps aux | grep ssserver
  ```
- Check if the port is occupied:
  ```bash
  netstat -plntu | grep 8388
  ```
- Disable the firewall or manually allow the port:
  ```bash
  systemctl stop firewalld
  ```
  or:
  ```bash
  firewall-cmd --permanent --add-port=8388/tcp
  firewall-cmd --permanent --add-port=8388/udp
  firewall-cmd --reload
  ```

### **2. Connection Fails?**
- Ensure `iptables` allows the necessary ports:
  ```bash
  iptables -I INPUT -p tcp --dport 8388 -j ACCEPT
  iptables -I INPUT -p udp --dport 8388 -j ACCEPT
  service iptables save
  ```
- Verify that `shadowsocks.json` has `"server": "0.0.0.0"` to allow external access.
- Double-check if your client settings match the server configuration.

---

## 9. Uninstall Shadowsocks
To remove Shadowsocks completely:
```bash
pip3 uninstall shadowsocks
rm -f /etc/shadowsocks.json
```

---

🎉 **Congratulations! Your Shadowsocks server is now set up and running on CentOS 7!**
```

