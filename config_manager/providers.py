import os
import json
import re

from config_manager.utils import run


PROTECTED_SUFFIX = 'PROTECTED'


def get_value(value):
    if isinstance(value, dict):
        value = json.dumps(value)

    return value


class Local:
    def __init__(self, context):
        self.context = context
        self.ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        self.command_prefix = ''
        self.command_suffix = ''

    @staticmethod
    def extract_key_attributes(name):
        is_protected = False
        if name.endswith(PROTECTED_SUFFIX):
            name = name.replace(f'_{PROTECTED_SUFFIX}', '')
            is_protected = True

        return is_protected, name

    def set_env_var(self, env_vars):
        for k, v in env_vars.items():
            _, env_var_name = self.extract_key_attributes(k)
            print(f'New Set local var: {env_var_name}={v}')
            os.environ[env_var_name] = v

    def run_command(self, command):
        command = f'{self.command_prefix} {command} {self.command_suffix}'
        return run(self.context, command)


class Heroku(Local):
    def __init__(self, context, app_name):
        Local.__init__(self, context)
        self.command_prefix = 'heroku'
        self.command_suffix = f'--app {app_name}'

        if not app_name:
            raise Exception('App name can not be empty')
        # Verify login
        command = f'access'
        self.run_command(command)

        self.reset_env_vars()

    def get_env_vars(self):
        command = f'config --json'
        result = self.run_command(command)
        return json.loads(self.ansi_escape.sub('', result.stdout))

    def reset_env_vars(self):
        current_vars = self.get_env_vars()
        if not current_vars:
            return

        command = f'config:unset {" ".join(current_vars.keys())}'
        self.run_command(command)

    def set_env_var(self, env_vars):
        env_vars_string = ''
        for k, v in env_vars.items():
            _, env_var_name = self.extract_key_attributes(k)
            env_vars_string += f' {env_var_name}={v}'

        # _, env_var_name = self.extract_key_attributes(name)
        command = f'config:set {env_vars_string}'
        self.run_command(command)


class TravisCI(Local):
    def __init__(self, context, travis_github_token):
        Local.__init__(self, context)
        self.command_prefix = 'travis'
        # Use --pro to force using travis-ci.org
        self.command_suffix = '--pro'

        command = f'login --github-token {travis_github_token}'
        self.run_command(command)

    def set_env_var(self, env_vars):
        command = f'env copy'
        protect_vars_command = ' --private'
        public_vars_command = ' --public'
        for k in env_vars.keys():
            is_protected, env_var_name = self.extract_key_attributes(k)

            if not is_protected:
                public_vars_command += f' {env_var_name}'
            else:
                protect_vars_command += f' {env_var_name}'

        print('----------------')
        print(command)
        self.run_command(f'{command} {public_vars_command}')
        self.run_command(f'{command} {protect_vars_command}')
