import _thread
import argparse
import time
import webbrowser
from threading import Thread

from git import Repo, InvalidGitRepositoryError, GitCommandError
from halo import Halo

from starmart.config.config import Config


class Action(object):
    def __init__(self, args):
        self.config = Config.default_config()
        self.args = args

    def act(self):
        raise NotImplementedError(f'act not implemented in {self.__name__}')

    @classmethod
    def get_action(cls):
        actions = dict({
            'deploy': DeployAction,
            'init': InitAction,
            'clone': CloneAction
        })

        args = cls.__parse_arguments__()
        action = actions.get(args.action[0])
        if action is None:
            raise ValueError('Action should be deploy, init or clone')

        return action(args)

    @classmethod
    def __parse_arguments__(cls):
        # configuring arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs=1, type=str, default='None',
                            help='Run init on a new project, deploy to push the code or clone <project_id> to retrieve an existing project')
        parser.add_argument('project_id', nargs='?', help='The project id', default=None)
        return parser.parse_args()


class InitAction(Action):

    def act(self):
        self.__auth_with_web_browser__()

    @Halo(text='Cloning starter code repo', spinner='dots')
    def __clone_default_code__(self):
        cloned = Repo.clone_from(self.config.github_repo(), 'starter_code')
        for r in cloned.remotes:
            if r.name == 'origin':
                cloned.delete_remote(r)
                break
        return cloned

    def __auth_with_web_browser__(self):
        webbrowser.open(f'{self.config.authentication_host()}/development/login')

        def callback(url):
            remote_host = self.config.git_remote_host()
            if not url.startswith(remote_host):
                raise ValueError(f'URL does not match the authentication host: {remote_host}')
            repo = self.__clone_default_code__()
            repo.create_remote('starmart', url=url)
            print('Happy coding!')

            # this is needed to exit flask server -> first it needs to return and then exit
            exit_after_seconds()

        # this blocks because of the server. that's why I set a callback
        from starmart.server.Server import server
        server(callback)


class DeployAction(Action):
    def act(self):
        self.__configure_repo__()

    @Halo(text='Pushing latest commits', spinner='dots')
    def __configure_repo__(self):
        repo = None
        try:
            repo = Repo('.')
            remote = None
            for r in repo.remotes:
                if r.name == 'starmart':
                    remote = r
                    break
            if remote is None:
                raise ValueError(f'The repository does not contain the starmart remote. Please call' +
                                 f' {bold("starmart init")}, before calling {bold("starmart deploy")}.')
            remote.push(refspec="main:main")
        except InvalidGitRepositoryError:
            raise ValueError('Github repository not initialized. Call starmart init before calling starmart deploy.')
        finally:
            print('\nPushed. Happy coding!')


class CloneAction(Action):

    def act(self):
        self.__clone_repo__()

    def __clone_repo__(self):
        project_id = self.args.project_id
        if project_id is None:
            raise ValueError(bold('starmart clone') + ' needs the project id')
        spinner = Halo(text=f'Cloning project {project_id}', spinner='dots')
        spinner.start()
        repo = Repo.clone_from(f'{self.config.git_remote_host()}/{project_id}.git', f'starmart_project_{project_id}')
        repo.remote('origin').rename('starmart')
        spinner.stop()
        print('Cloned. Happy coding!')


def exit_after_seconds(seconds=2):
    def do_exit():
        time.sleep(seconds)
        _thread.interrupt_main()

    Thread(target=do_exit).start()


def bold(text):
    return '\033[1m' + text + '\033[0m'


def main():
    Action.get_action().act()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
