# git 
ssh-keygen
git@github.com:yk-st/flask_sample_apps.git

# アップデート
sudo apt update

# dockerの準備
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release -y
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
sudo usermod -aG docker $USER 
newgrp docker

sudo apt-get install htop

# ssh
sudo vim /etc/ssh/sshd_config
ClientAliveInterval 120

# docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# git
git config --global user.name "yk-st"
git config --global user.email "mail"

alias gall='git add -A && git commit -m '\''commit'\'' && git push origin main'

# build
alias build='git pull;docker-compose build;docker-compose up -d'

#
https://udemy-flask-sample.top/setting/

# command
docker exec -it udemy-flask-sample_app_1 /bin/bash

# keycloak 
 SSO session idle timeout変更

# サインアウト(Oauth2proxyからサインアウトしてその後にKeyCloakのサインアウト画面に遷移する)
https://udemy-flask-sample.top/oauth2/sign_out?rd=https%3A%2F%2Fauth.udemy-flask-sample.top%3A8443%2Frealms%2Fhogepeke%2Fprotocol%2Fopenid-connect%2Flogout/

# トークン取得系のコマンド
curl -k -X POST \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "grant_type=client_credentials&scope=openid" \
        -d "client_id=flasks" \
        -d "client_secret=G6xqdoC33HytUhEi0vjvUgKMSGZ2QXYL" \
         "https://auth.udemy-flask-sample.top:8443/realms/hogepeke/protocol/openid-connect/token"

# トークンが有効化を確認する
curl -k \
     -X POST \
     -u "flasks:G6xqdoC33HytUhEi0vjvUgKMSGZ2QXYL" \
     -d "token=$TOKEN" \
   "https://auth.udemy-flask-sample.top:8443/realms/hogepeke/protocol/openid-connect/token/introspect"

# flaskのルート確認
flask routes

# 返却したいJSON
```
{
    "resource": {
        "id": "aaa",
        "address": {
            "zip": "peke",
            "postal": "maruo"
        },
        "addresses": [
            {
                "id": 1,
                "zip": "peke",
                "postal": "maruo"
            },
            {
                "id": 2,
                "zip": "pekeo",
                "postal": "maruo2"
            }
        ]
    }
}
```

# actions
docker exec -it udemy-flask-sample_app_api_1 /bin/bash -c "pytest tests/test_hoge.py -s"

https://hsmtweb.com/tool-service/github-actions.html