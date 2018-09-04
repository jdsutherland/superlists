Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv


## restarting

    sudo systemctl daemon-reload
    sudo systemctl reload nginx
    sudo systemctl enable gunicorn-superlists-staging.us
    sudo systemctl start gunicorn-superlists-staging.us.service

sed "s/SITENAME/superlists-staging.us/g" source/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/superlists-staging.us

## testing staging server (from local)
> TODO: move to main README
STAGING_SERVER=superlists-staging.us python manage.py test functional_tests
