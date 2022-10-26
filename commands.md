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

# サインアウト
https://udemy-flask-sample.top/oauth2/sign_out?rd=https://login.udemy-flask-sample.top:8443/realms/hogepeke/protocol/openid-connect/logout

# actions
 https://hsmtweb.com/tool-service/github-actions.html