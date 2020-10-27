Privisioning a new site
-----------------------
-----------------------

##required packages:

*nginx
*python3.8
*virtualenv + pip
*Git

eg, on Ubuntu:
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt-get install nginx git python3.8 python3.8-venv

##Nginx virtual host config
	* see nginx.template.conf
	* replace SITENAME with, e.g., mydomain.ir

##Systemd service
	* see gunicorn-systemd.template.service
	* replace SITENAME with, e.g., mydomain.com
	* replace SEKRIT with email password

## Folder structure:
	Assume we have a user account at /home/username
	/home/username
	└── sites
		└── SITENAME
			├── database
			├── source
			└── virtualenv
