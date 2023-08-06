import configparser
import os
import argparse
from appdirs import user_data_dir

from taskimporter import const
from taskimporter.task import Task
from taskimporter.services import JiraService, GithubService, GitlabService
from taskimporter.things3_utils import add_to_things
from taskimporter.omnifocus3_utils import add_to_omnifocus


def configure_services(config, user_services):
    s_list = []

    for service in user_services:
        if config[service]['service'] == 'jira':
            server = config[service]['server']
            api_token = config[service]['api_token']
            project = config[service]['project']
            jira = JiraService(server, api_token, project)

            s_list.append(jira)
        elif config[service]['service'] == 'github':
            repo = config[service]['repo']
            api_token = config[service]['api_token']
            project = config[service]['project']
            github = GithubService(repo, api_token, project)

            s_list.append(github)

        elif config[service]['service'] == 'gitlab':
            gitlab_instance = config[service]['gitlab_instance']
            repo = config[service]['repo']
            api_token = config[service]['api_token']
            project = config[service]['project']
            gitlab = GitlabService(gitlab_instance, repo, api_token, project)

            s_list.append(gitlab)

    return s_list


def main():
    parser = argparse.ArgumentParser(description='Import tasks from various services')
    parser.add_argument('-c', '--config', help='Path to configuration file')
    parser.add_argument('-w', '--write', help='Write default config', action='store_true')
    args = parser.parse_args()

    config_path = user_data_dir('taskimporter', 'Joshua Mulliken') + '/config.ini'

    if args.config:
        config_path = args.config

    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    if args.write:
        with open(config_path, 'w') as f:
            f.write(const.DEFAULT_CONFIG)

            print('Default config written to \"{}\"'.format(config_path))
            print('Please edit the config file and run again')
            exit(0)

    config = configparser.ConfigParser()

    task_manager = ""
    user_services = []

    try:
        config.read(config_path)
        task_manager = config['DEFAULT']['task_manager']
        user_services = [section for section in config.sections() if section != 'DEFAULT']
    except KeyError:
        print('Invalid config file')
        print('Please run with --write to create a default config file')
        print('Config file path: \"{}\"'.format(config_path))
        exit(1)

    if len(user_services) == 0:
        print("No services configured. Please add a service to the config file and run again")
        print("Config location: \"{}\"".format(config_path))
        exit(0)

    for service in configure_services(config, user_services):
        print("Refreshing tasks from %s" % service.name)
        for task in service.get_tasks():
            print("Adding task: %s" % task.name)
            if task_manager == 'things3':
                add_to_things(task, service.project_key)
            elif task_manager == 'omnifocus3':
                add_to_omnifocus(task, service.project_key)


if __name__ == "__main__":
    main()
