# "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"
# mkdir -p /run/nginx && touch /run/nginx/nginx.pid
# /usr/sbin/php-fpm7
# /usr/sbin/nginx -c /etc/nginx/nginx.conf -g 'daemon off;'

chmod 777 /run /var/lib/nginx /var/log/nginx /var/log/php7 /tmp
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf