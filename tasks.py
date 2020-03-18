import os

from invoke import task

from config_manager.providers import Heroku, TravisCI, Local
from config_manager.utils import load_yaml_from_file, BASEDIR, run

DEV_ENV_NAME = 'dev'
SETTINGS_EXT = 'yml'
SECRETS_PATH = os.path.join(BASEDIR, '..', '.gitsecret')
SETTINGS_PATH = os.path.join(SECRETS_PATH, 'settings')


def get_settings_filename(env):
    return f'{env}.{SETTINGS_EXT}'


def get_settings_filepath(filename):
    return os.path.join(SETTINGS_PATH, get_settings_filename(filename))


@task()
def create_new_secure_config_file(c, filename):
    filepath = get_settings_filepath(filename)

    # Raise exception is file already exists
    with open(filepath, 'x'):
        pass

    run(c, f'git secret add {filepath}')


@task()
def set_vars(c, settings=None):
    env_vars = load_yaml_from_file(os.path.join(SETTINGS_PATH, get_settings_filename(DEV_ENV_NAME)))

    if settings and settings != 'dev':
        env_vars.update(load_yaml_from_file(os.path.join(SETTINGS_PATH, get_settings_filename(settings))))

    def get_env_ver_value(key_name, remove=False):
        if remove:
            env_value = env_vars.pop(key_name)
        else:
            env_value = env_vars.get(key_name)

        return env_value

    heroku_app_name = get_env_ver_value('HEROKU_APP_NAME', remove=True)
    travis_github_token = get_env_ver_value('TRAVIS_GITHUB_TOKEN', remove=True)

    local_client = Local(c)
    heroku_client = Heroku(c, heroku_app_name)
    travis_client = TravisCI(c, travis_github_token)

    local_client.set_env_var(env_vars)
    heroku_client.set_env_var(env_vars)
    travis_client.set_env_var(env_vars)
