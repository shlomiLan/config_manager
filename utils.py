import os

import yaml

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


def run(c, command, with_venv=False, warn_only_not_fail=False):
    if with_venv:
        command = '{} && {}'.format(get_venv_action(), command)

    print('Running: {}'.format(command))
    return c.run(command, warn=warn_only_not_fail, pty=True)


def load_yaml_from_file(file_path):
    with open(file_path, 'r') as stream:
        return yaml.safe_load(stream)


def is_unix():
    return os.name == 'posix'


def get_venv_action():
    if is_unix():
        return f'source {BASEDIR}/venv/bin/activate'
    else:
        return f'{BASEDIR}\\venv\\Scripts\\activate'
