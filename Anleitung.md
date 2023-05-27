# Anleitung zur Einrichtung eines virtuellen Servers

Hier sind die Schritte, um deinen virtuellen Server einzurichten und ein FastAPI-Projekt zu starten.

## Erstellen eines neuen Benutzers

Führe die folgenden Befehle aus, um einen neuen Benutzer zu erstellen und diesen zum Superuser zu machen:

```bash
adduser fastapi
usermod -aG sudo fastapi
su – fastapi
```

# Docker-Setup

Führe diese Befehle aus, um Docker auf deinem Ubuntu-System zu installieren. Hier ist die Docker Installationsanleitung: https://docs.docker.com/engine/install/ubuntu/

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

# Certbot Installation

```bash
sudo apt-get install certbot python3-certbot-nginx
certbot –certonly
```

# Projekt starten

```bash
systemctl stop nginx
git clone https://github.com/Coding-Crashkurse/TwitterClone-FastAPI.git -b deployment
docker compose up --build

```
