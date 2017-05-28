import docker
from xqueue_watcher.grader import Grader
import shutil
import os
import json

# DOCKER_IMAGE = 'zhipengyan/ucsdx:docker-grader'
DOCKER_IMAGE = 'zhipengyan/ucsdx:test'
COURSE_VOLUME = {'/home/ubuntu/edX-extensions/edX-nbgrader/dummy-course': {'bind': '/app/dummy-course', 'mode': 'rw'}}

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
        results = c.containers.run(DOCKER_IMAGE, remove=True, command=command_str, volumes=COURSE_VOLUME)
        try:
            results = eval(results)
        except Exception as e:
            results = json.loads(results)
        results.update({'tests':'', 'errors':''})
        return results

if __name__ == "__main__":
    d = DockerGrader()
    sample_nb = 'https://raw.githubusercontent.com/jupyter/nbgrader/master/nbgrader/docs/source/user_guide/source/ps1/problem1.ipynb'
    print '********* dummy test *********'
    print d.grade('ps1/problem1', '{"problem1.ipynb": "http://asdf.com"}', '')
    print '********* grading test *********'
    print d.grade('ps1/problem1', '{{"problem1.ipynb": "{}"}}'.format(sample_nb), '')
