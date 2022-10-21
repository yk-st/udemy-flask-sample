FROM nginx:1.23.1

# Time Zone
# タイムゾーン、ロケール設定
ENV TZ="Asia/Tokyo" \
    LANG="C.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="C.UTF-8"

COPY default.conf /etc/nginx/conf.d/