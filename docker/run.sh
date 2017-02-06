/usr/sbin/service ssh start
/usr/sbin/service riak start
/usr/sbin/service rabbitmq-server start
/usr/sbin/service celeryd start
/usr/sbin/service nginx start
/data/venv/bin/uwsgi --ini /data/etc/uwsgi.ini --pidfile /run/uwsgi.pid --daemonize /data/logs/uwsgi_daemon.log
