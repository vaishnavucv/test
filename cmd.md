# ActiveMQ 5.18.2 — Installation & Configuration Commands (Ubuntu, Markdown)

> Scope: install **apache-activemq-5.18.2** from the official archive, lock down listeners to **127.0.0.1**, rotate console creds, and (optionally) run as a **systemd** service. Works on Ubuntu 20.04/22.04/24.04.

---

## 0) Prerequisites & Host Hygiene

```bash
# Update packages and install Java 11 and basic tools
sudo apt-get update
sudo apt-get install -y openjdk-11-jre-headless curl tar gnupg coreutils

# Verify Java is present
java -version

# Create a dedicated system user and base directories
sudo useradd --system --home /opt/activemq --shell /usr/sbin/nologin activemq
sudo mkdir -p /opt/activemq/{dist,versions}
sudo chown -R activemq:activemq /opt/activemq
```

---

## 1) Download 5.18.2 + Integrity Verification

```bash
# Work in the distribution directory
cd /opt/activemq/dist

# Pull the tarball + hashes + PGP signature from Apache archive
sudo -u activemq bash -lc '
  curl -O https://archive.apache.org/dist/activemq/5.18.2/apache-activemq-5.18.2-bin.tar.gz
  curl -O https://archive.apache.org/dist/activemq/5.18.2/apache-activemq-5.18.2-bin.tar.gz.sha512
  curl -O https://archive.apache.org/dist/activemq/5.18.2/apache-activemq-5.18.2-bin.tar.gz.asc
'

# SHA512 verification
sha512sum -c apache-activemq-5.18.2-bin.tar.gz.sha512

# Optional PGP verification (imports Apache KEYS)
curl -s https://downloads.apache.org/activemq/KEYS | gpg --import
# Expect: 'Good signature from ...' on verify
gpg --verify apache-activemq-5.18.2-bin.tar.gz.asc apache-activemq-5.18.2-bin.tar.gz || true
```

---

## 2) Extract & Activate Current Symlink

```bash
# Extract under versions/ and create a stable "current" symlink
sudo -u activemq bash -lc '
  tar -xzf /opt/activemq/dist/apache-activemq-5.18.2-bin.tar.gz -C /opt/activemq/versions
  ln -sfn /opt/activemq/versions/apache-activemq-5.18.2 /opt/activemq/current
'

# Confirm layout
ls -l /opt/activemq
```

---

## 3) Lock Down OpenWire (bind to 127.0.0.1)

> Default OpenWire connector listens on `0.0.0.0:61616`. We pin it to `127.0.0.1:61616` to avoid exposure.

```bash
# Backup original broker config
sudo -u activemq bash -lc 'cp /opt/activemq/current/conf/activemq.xml /opt/activemq/current/conf/activemq.xml.bak.$(date +%F)'

# Replace OpenWire listener with loopback bind
sudo -u activemq bash -lc "sed -i 's#uri=\"tcp://0.0.0.0:61616#uri=\"tcp://127.0.0.1:61616#g' /opt/activemq/current/conf/activemq.xml"

# (Optional) also limit MQTT/AMQP/WS if enabled in your build
# Example patterns (uncomment and adapt if connectors exist):
# sudo -u activemq sed -i 's#tcp://0.0.0.0:1883#tcp://127.0.0.1:1883#g' /opt/activemq/current/conf/activemq.xml
# sudo -u activemq sed -i 's#amqp://0.0.0.0:5672#amqp://127.0.0.1:5672#g'   /opt/activemq/current/conf/activemq.xml
```

---

## 4) Lock Down Web Console (Jetty bind to 127.0.0.1)

> The embedded Jetty typically binds to `0.0.0.0` on port `8161`. We bind to localhost.

```bash
# Backup Jetty config
sudo -u activemq bash -lc 'cp /opt/activemq/current/conf/jetty.xml /opt/activemq/current/conf/jetty.xml.bak.$(date +%F)'

# Force Jetty host to 127.0.0.1 (change default host)
sudo -u activemq bash -lc "sed -i 's#default=\"0.0.0.0\"#default=\"127.0.0.1\"#g' /opt/activemq/current/conf/jetty.xml"

# (Optional) change port if 8161 is occupied
# sudo -u activemq bash -lc "sed -i 's#<Set name=\"port\">.*#<Set name=\"port\">8161<\\/Set>#' /opt/activemq/current/conf/jetty.xml"
```

---

## 5) Rotate Web Console Credentials

> Default users are `admin: admin` and `user: user` in `jetty-realm.properties`. Replace with strong secrets.

```bash
# Backup realm file
sudo -u activemq bash -lc 'cp /opt/activemq/current/conf/jetty-realm.properties /opt/activemq/current/conf/jetty-realm.properties.bak.$(date +%F)'

# Generate strong random passwords
ADMIN_PW=$(openssl rand -base64 24)
USER_PW=$(openssl rand -base64 20)
echo "[INFO] Admin PW: $ADMIN_PW"; echo "[INFO] User PW: $USER_PW"

# Overwrite with new credentials (roles: admin and user)
sudo -u activemq bash -lc "cat > /opt/activemq/current/conf/jetty-realm.properties <<'EOF'
# ActiveMQ Web Console users (username: password, role)
admin: $ADMIN_PW, admin
user:  $USER_PW, user
EOF"
```

> Save the printed passwords securely. To set explicit values instead of random, replace `$ADMIN_PW`/`$USER_PW` inline.

---

## 6) Run in Foreground (Lab Mode)

```bash
# Foreground/console mode for interactive labs
sudo -u activemq bash -lc '
  cd /opt/activemq/current
  bin/activemq console
'
```

Open another terminal for validation.

```bash
# Confirm listeners are loopback-only
ss -ltnp | grep -E ':61616|:8161'

# Quick console check (expects HTTP 200, then Ctrl+C)
curl -I http://127.0.0.1:8161/ || true

# If needed, authenticate to the admin page in a browser
# URL: http://127.0.0.1:8161/admin
```

> Stop foreground run with `Ctrl+C`.

---

## 7) Install as a systemd Service (Optional)

```bash
# Create systemd unit file
sudo tee /etc/systemd/system/activemq.service > /dev/null <<'UNIT'
[Unit]
Description=Apache ActiveMQ 5.18.2
After=network.target

[Service]
Type=forking
User=activemq
Environment=JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
Environment=ACTIVEMQ_HOME=/opt/activemq/current
Environment=ACTIVEMQ_BASE=/opt/activemq/current
PIDFile=/opt/activemq/current/data/activemq.pid
ExecStart=/opt/activemq/current/bin/activemq start
ExecStop=/opt/activemq/current/bin/activemq stop
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
UNIT

# Reload, enable, and start
sudo systemctl daemon-reload
sudo systemctl enable --now activemq
sudo systemctl status activemq --no-pager
```

Service management:

```bash
# Start/stop/restart/status
sudo systemctl start activemq
sudo systemctl stop activemq
sudo systemctl restart activemq
sudo systemctl status activemq --no-pager
```

---

## 8) Validation & Version Proof

```bash
# Show version from startup log (one liner)
grep -m1 -E 'ActiveMQ.*5\.18\.2' /opt/activemq/current/data/activemq.log || tail -n 50 /opt/activemq/current/data/activemq.log

# Curl the console root (HTTP 200 expected)
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8161/

# (If Jolokia is enabled in your image) read Broker version via Jolokia MBean
# curl -u admin:${ADMIN_PW} -s \
#  'http://127.0.0.1:8161/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost/Version'
```

---

## 9) Rollback / Cleanup

```bash
# Stop service if running
sudo systemctl stop activemq || true

# Remove service unit
sudo systemctl disable activemq || true
sudo rm -f /etc/systemd/system/activemq.service
sudo systemctl daemon-reload

# Remove installation (irreversible)
sudo rm -rf /opt/activemq
sudo userdel activemq || true
```

---

## 10) Optional: Side‑by‑side A/B (5.18.2 vs 5.18.3) in Docker

> For remediation validation without touching the host, you can A/B test using Compose.

```yaml
# docker-compose.yml
version: "3.8"
services:
  amq-vuln:
    image: apache/activemq-classic:5.18.2
    container_name: amq-vuln
    ports:
      - "127.0.0.1:61616:61616"  # OpenWire
      - "127.0.0.1:8161:8161"    # Web console

  amq-fixed:
    image: apache/activemq-classic:5.18.3
    container_name: amq-fixed
    ports:
      - "127.0.0.1:61617:61616"  # OpenWire (offset)
      - "127.0.0.1:8162:8161"    # Web console (offset)
```

```bash
# Run the pair locally (loopback-only bindings)
docker compose up -d

# Validate ports
ss -ltnp | grep -E ':6161(6|7)|:816(1|2)'
```

---

### Notes

* Keep **all** listeners bound to `127.0.0.1` during testing.
* When your lab is complete, repeat install with **5.18.3+** to verify remediation behaviors.
* For headless servers without GUI, use `curl` or `lynx` to sanity-check the web console endpoint.
