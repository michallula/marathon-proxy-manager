# marathon-proxy-manager

Nginx proxy and load-balancing settings management automation for marathon mesos environment.

## About

This tool generates *Nginx* server configuration base on available *Marathon* tasks. It fetches all *Marathon* tasks 
via marathon REST api, then groups it by application. For each application it produces *Nginx* server definition file. 
This file, contains by default, reverse proxy and load balancing definition (you can customise this behaviour by providing
your own config file template). Default server definition assumes that application will be launch using subdomain 
(ex. sample-app application will be called with http://sample-app.some-domain.com). It redirects to one of the hosts on
which the application is deployed. 

## Installation

To install type in terminal

`pip install marathon-proxy-manager`

## Execution

After installation you may launch it using following command:

`python -m marathon_proxy_manager --marathon-url http://some-domain:8080 --domain some-domain --delete-unused --override --reload`

You should run it with sufficient privileges to write to your *Nginx* configuration directory and to call `service nginx reload` 
command (or you can provide `--out-dir` option and ).

To run this as a cron job add this line to the */etc/crontab*:
 
`* *    * * *   root    python -m marathon_proxy_manager --marathon-url http://some-domain:8080 --domain some-domain --delete-unused --override --reload 2> /var/log/marathon_proxy_manager/err.log > /var/log/marathon_proxy_manager/out.log`

## Options

To show all options type:

`python -m marathon_proxy_manager -h`


