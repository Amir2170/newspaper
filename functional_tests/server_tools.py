from os import path
import subprocess
THIS_FOLDER = path.dirname(path.abspath(__file__))


def reset_database(host):
	subprocess.check_call(
		['fab', 'reset_database', f'--host=amir@{host}'],
		cwd=THIS_FOLDER,
	)


def create_session_on_server(host, username, password):
	subprocess.check_output(
		[
			'fab', 
			f'create_session_on_server:username={username} password={password}',
			f'--host=amir@{host}',
			'--hide=everything, status',
		],
		cwd=THIS_FOLDER
	).decode().strip()
