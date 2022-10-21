# ドメインの取得
サブドメを取得する

#　サーバーへのログイン


# git 
ssh-keygen
git@github.com:yk-st/flask_sample_apps.git


# 初期設定コマンド

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

# git ignore
何か除外する

# レクチャー80
flask route
で、docのページを確認するようにすればOK


# HTMLのテンプレを用意する

1. 認証認可までは動画を取ってしまう。セクション８まで録画をしてしまう。


2. Viewの部分は、該当部分を紹介するだけにして、モックで画面が移動できるようにすればいい
そこからロジック部分をいくつか作り込んでいくイメージ

レクチャー54は最後に録画する。

一旦作りきって、フォームとかを歯抜けの状態にして行く感じ。


# keycloak 
 SSO session idle timeou をちゃんと変えておく。


# actions
 https://hsmtweb.com/tool-service/github-actions.html