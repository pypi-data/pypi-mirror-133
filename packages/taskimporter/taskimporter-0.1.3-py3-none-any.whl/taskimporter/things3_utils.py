from subprocess import Popen, PIPE

from taskimporter import Task

THINGS_PROJECT = "Default Project"
APPLESCRIPT_FORMAT_STRING = """
tell application \"Things3\"
    if \"{todo_name}\" is not in (name of every to do in project \"{things_project}\") then
        set TheTodo to (make to do at project \"{things_project}\")
        set name of TheTodo to \"{todo_name}\"
        set notes of TheTodo to \"{todo_url}\"
    end if
end tell
"""


def add_to_things(task: Task, things_project=THINGS_PROJECT):
    with Popen(['osascript', '-'], stdin=PIPE) as proc:
        proc.stdin.write(APPLESCRIPT_FORMAT_STRING.format(
            todo_name=task.name,
            todo_url=task.url,
            things_project=things_project
        ).encode('utf-8'))
        proc.stdin.close()
        proc.wait()