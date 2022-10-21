#!/bin/bash

{
    echo "---- start renew-cert $(date '+%Y-%m-%d %H:%M:%S')"

    cd /root/children-money || exit 1

    hoge=$(docker-compose run --rm certbot renew --post-hook='echo hoge' 2>&1)

    if echo "${hoge}" | grep -q "hoge"; then
        docker-compose exec -T nginx nginx -s reload
    fi

} >> /var/log/renew-cert.log 2>&1