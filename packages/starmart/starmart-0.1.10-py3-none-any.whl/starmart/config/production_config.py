from starmart.config.config import Config


class ProductionConfig(Config):
    def github_repo(self) -> str:
        return 'git@github.com:starmart-io/Model-Template.git'

    def authentication_host(self) -> str:
        return 'https://starmart.io'

    def git_remote_host(self):
        return 'git@gitlab.com:starmart/user-uploaded-mappers-and-models'
