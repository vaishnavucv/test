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

# SHA
```
