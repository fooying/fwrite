export PYTHONPATH=/opt
ps -ef|grep 'uwsgi -s :11000'|grep -v grep |awk '{print $2} '|xargs kill -9
uwsgi -s :11000 -w index -p 2 -d /data/log/www/uwsgi_fwrite.log -M -p 4  -t 30  -R 11000 
