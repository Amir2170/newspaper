from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
import os


REPO_URL = 'https://github.com/Amir2170/newspaper.git'

def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database', 'virtualenv', 'source'):
		run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
	if exists(source_folder + '/newspaper/.git'):
		run(f'cd {source_folder}/newspaper && git fetch')
	else:
		run(f'cd {source_folder} && git clone -b master {REPO_URL}')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	run(f'cd {source_folder}/newspaper && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/newspaper/newspaper_project/settings.py'
	sed(settings_path, "DEBUG=True", "DEBUG=False")
	sed(settings_path,
		"ALLOWED_HOSTS = .+$",
		f'ALLOWED_HOSTS = ["{site_name}"]',
	)
	secret_key_file = source_folder + '/newspaper/newspaper_project/secret_key.py'
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, f'SECRET_KEY = "{key}"')
	append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder +'/bin/pip3.8'):
		run(f'python3.8 -m venv {virtualenv_folder}')
	run(f'{virtualenv_folder}/bin/pip3.8 install -r {source_folder}/newspaper/requirments.txt')
		

def _update_database(source_folder):
	run(
		f'cd {source_folder}/newspaper'
		' && ../../virtualenv/bin/python3.8 manage.py migrate --noinput'
	)


def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	source_folder = site_folder + '/source'
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_database(source_folder)

