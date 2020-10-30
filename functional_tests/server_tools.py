from os import path
import subprocess
THIS_FOLDER = path.dirname(path.abspath(__file__))
from fabric.api import env

env.key_filename = "/path/to/.ssh/ssk_non_public_key"


def reset_database(host):
    subprocess.check_call(
        ['fab', 'reset_database', '--host=amir@{}'.format(host)],
        cwd=THIS_FOLDER
    )


def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            'fab',
            f'create_session_on_server:username:{username}',
            '--host=amir@{}'.format(host),
            '--hide=everything,status',
        ],
        cwd=THIS_FOLDER
    ).decode().strip()
