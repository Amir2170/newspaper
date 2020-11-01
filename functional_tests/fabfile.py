from fabric.api import env, run


def _get_base_folder(host):
	return '~/sites/' + host
	
	
def _get_manage_dot_py(host):
	return  f'{_get_base_folder(host)}/virtualenv/bin/python3.8 {_get_base_folder(host)}/source/newspaper/manage.py'
		


def reset_database():
	run(f'{_get_manage_dot_py(env.host)} flush --noinput')


def create_session_on_server(username, password):
	session_key = run(
		f'{_get_manage_dot_py(env.host)} create_session {username} {password}'
	)
	print(session_key)
