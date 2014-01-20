export PYTHONPATH=/opt
ps -ef|grep 'uwsgi -s :10000'|grep -v grep |awk '{print $2} '|xargs kill -9
uwsgi -s :10000 -w index -p 2 -d /data/log/www/uwsgi_xssing.log -M -p 4  -t 30  -R 10000 
