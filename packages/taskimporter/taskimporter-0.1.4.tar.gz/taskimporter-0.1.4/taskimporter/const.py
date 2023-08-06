DEFAULT_CONFIG = \
"""# This is the default configuration file for the task importer.
# The following settings are required:
[DEFAULT]
task_manager=things3

# The following settings are examples of services that can be imported.
# You can add as many services as you want.
; [Work Jira]
; service=jira
; server=https://jira.example.com
; api_token=<ACCESS_TOKEN>
; project=<PROJECT_KEY>
 
; [Work Github]
; service=github
; repo=<REPO_NAME>
; api_token=<ACCESS_TOKEN>
; project=<PROJECT_KEY>

; [Work Gitlab]
; service=gitlab
; gitlab_instance=<INSTANCE>
; repo=<REPO_NAME>
; api_token=<ACCESS_TOKEN>
; project=<PROJECT_KEY>
"""
