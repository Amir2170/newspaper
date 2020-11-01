from fabric.api import env, run


def _get_base_folder(host):
	return '~/sites/' + host
	
	
def _get_manage_dot_py(host):
	base_folder = _get_base_folder(host)
	return  f'{base_folder}/virtualenv/bin/python3.8 {base_folder}/source/newspaper/manage.py'
		


def reset_database():
	manage_dot_py = _get_manage_dot_py(env.host)
	run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(username, password):
	manage_dot_py = _get_manage_dot_py(env.host)
	session_key = run(
		f'{manage_dot_py} create_session username={username} password={password}'
	)
