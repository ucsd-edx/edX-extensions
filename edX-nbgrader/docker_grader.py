import docker
from xqueue_watcher.grader import Grader
import shutil
import os
import json


class DockerGrader(Grader):
    """
    self.grader_root should be set to the course root
    """

    def grade(self, payload, files, _):
        section_name, problem_name = payload.split('/')
        files = json.loads(files)
        submission_url = files.values()[0]

        command_str = 'python2.7 grade.py {} {} {}'.format(section_name, problem_name, submission_url)
        c = docker.from_env()
        results = c.containers.run('zhipengyan/ucsdx:docker-grader', remove=True, command=command_str)
        results = eval(results)
        results.update({'tests':'', 'errors':''})
        return results

if __name__ == "__main__":
    d = DockerGrader()
    print d.grade('ps1/problem1', 'http://asdf.com', '')
