from abc import abstractmethod
from typing import List

from jira import JIRA
from jira.resources import Issue as JiraIssue
from github import Github
from gitlab import Gitlab

from taskimporter import Task


class BaseService:
    name: str
    project_key: str

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_tasks(self) -> List[Task]:
        pass


class JiraService(BaseService):
    def __init__(self, server, token_auth, project_key):
        self._server = server
        self._jira = JIRA(server=self._server, token_auth=token_auth)
        self.name = "Jira: %s" % self._server
        self.project_key = project_key

    def get_tasks(self):
        issues = self._jira.search_issues('assignee = currentUser() AND resolution = Unresolved')

        tasks = []
        issue: JiraIssue
        for issue in issues:
            task = Task()
            task.name = "[%s] %s" % (issue.key, issue.fields.summary)
            task.url = "%s/browse/%s" % (self._server, issue.key)

            tasks.append(task)

        return tasks


class GithubService(BaseService):
    def __init__(self, repo_name, access_token, project_key):
        """
        Create a GitHub Service instance for a particular repo.

        :param access_token: Your GitHub access token.
        :param repo_name: The repository you would like to get tasks from. (<USER>/<REPO>)
        """
        self._github = Github(access_token)
        self._repo_name = repo_name
        self._repo = self._github.get_repo(repo_name)

        self.name = "GitHub: %s" % repo_name
        self.project_key = project_key

    def get_tasks(self) -> List[Task]:
        issues = self._repo.get_issues(state='open')
        pull_requests = self._repo.get_pulls(state='open')

        tasks = []
        for issue in issues:
            task = Task()
            task.name = "[Issue] %s" % issue.title
            task.url = issue.html_url

            tasks.append(task)

        for pull_request in pull_requests:
            task = Task()
            task.name = "[Pull Request] %s" % pull_request.title
            task.url = pull_request.html_url

            tasks.append(task)

        return tasks


class GitlabService(BaseService):
    def __init__(self, gitlab_instance, repo_name, access_token, project_key):
        self._gitlab = Gitlab(gitlab_instance, private_token=access_token)
        self._gitlab.auth()
        self._repo_name = repo_name
        self._repo = self._gitlab.projects.get(repo_name)

        self.name = "GitLab: %s" % repo_name
        self.project_key = project_key

    def get_tasks(self) -> List[Task]:
        issues = self._repo.issues.list(state='opened')
        merge_requests = self._repo.mergerequests.list(state='opened')

        tasks = []
        for issue in issues:
            task = Task()
            task.name = "[Issue] %s" % issue.title
            task.url = issue.web_url

            tasks.append(task)

        for merge_request in merge_requests:
            task = Task()
            task.name = "[Pull Request] %s" % merge_request.title
            task.url = merge_request.web_url

            tasks.append(task)

        return tasks
