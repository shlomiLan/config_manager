from invoke import Context
from config_manager.providers import Heroku


class TestHeroku:
    def test_new(self):
        assert 1 == 2

    heroku_app_name = 'test1-shlomi'
    context = Context()
    heroku = Heroku(context, heroku_app_name)
#
#     def test_reset_vars(self):
#         env_vars = {
#             'xxx': 'yyy'
#         }
#
#         self.heroku.set_env_var(env_vars)
#         current_vars = self.heroku.get_env_vars()
#         assert current_vars == env_vars
#
#         self.heroku.reset_env_vars()
#         current_vars = self.heroku.get_env_vars()
#         assert not current_vars
