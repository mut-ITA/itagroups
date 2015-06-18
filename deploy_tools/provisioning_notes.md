Provisioning a new site
=======================

## Required Packages

* nginx
* python3
* pip
* git
* virtualenv

to get them (Ubuntu):

	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

## nginx virtual host config
* see nginx.template.conf
* replace SITENAME with, eg staging.mydomain.com
		  USERNAME with, eg ghust1995

## Upstart Job
* see gunicorn-upstart.template.conf
* replace SITENAME with, eg staging.mydomain.com
		  USERNAME with, eg ghust1995
		  DJANGOPROJECTNAME with, eg itagroups

## Folder Structure:
User account at /home/USERNAME

/home/USERNAME
|-- sites
	|-- SITENAME
		|-- database
		|-- source
		|-- static
		|-- virtualenv