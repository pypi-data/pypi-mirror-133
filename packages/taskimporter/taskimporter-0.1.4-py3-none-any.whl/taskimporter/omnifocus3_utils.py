from subprocess import Popen, PIPE

from taskimporter import Task

# look for an existing project with the same name and if one doesn't exist,
# create it
OMNIFOCUS_PROJECT="Default Project"
APPLESCRIPT_FORMAT_STRING = """
tell front document of application \"OmniFocus\"
    set ExistingProject to false
    set theProjects to every flattened project where its completed = false
    repeat with a from 1 to length of theProjects
        set currentProj to item a of theProjects
        set nameProj to name of currentProj
        if \"{omnifocus_project}\" = nameProj then
            set ExistingProject to true
            set UseProject to currentProj
        end if
    end repeat

    if not ExistingProject then
        set UseProject to make new project with properties {{name:\"{omnifocus_project}\", singleton action holder:true}}
    end if
    if \"{todo_name}\" is not in (name of every flattened task of currentProj where its completed = false) then
        tell UseProject
            set theTask to make new task with properties {{name:\"{todo_name}\", note:\"{todo_url}\"}}
        end tell
    end if
end tell
"""


def add_to_omnifocus(task: Task, omnifocus_project=OMNIFOCUS_PROJECT):
    with Popen(['osascript', '-'], stdin=PIPE) as proc:
        proc.stdin.write(APPLESCRIPT_FORMAT_STRING.format(
            todo_name=task.name,
            todo_url=task.url,
            omnifocus_project=omnifocus_project
        ).encode('utf-8'))
        proc.stdin.close()
        proc.wait()

