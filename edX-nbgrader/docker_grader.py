import docker
from xqueue_watcher.grader import Grader
from nbgrader.api import *
import shutil
import os
import json
import random

"""
    GLOBALS
"""
# DOCKER_IMAGE = 'zhipengyan/ucsdx:docker-grader'
DOCKER_IMAGE = 'zhipengyan/ucsdx:docker-grader-v2'
COURSE_NAME = 'dummy_course'
COURSE_DIR = '/home/ubuntu/edX-extensions/edX-nbgrader/dummy-course'


class DockerGrader(Grader):
    """
    self.grader_root should be set to the course root
    """
    def __init__(self, grader_root-='/app/dummy-course', fork_per_item=True, logger_name=__name__):
        super(Grader, self).__init__(grader_root, fork_per_item, logger_name)
        self.gradebook = os.path.join(self.grader_root, 'gradebook.db')
        if not os.path.isfile(self.gradebook):
            print 'Error finding course book'
        self.gb = GradeBook('sqlite:///' + self.graderbook)

    def _handle_result(self, result_str, error_msg):
        result = {}
        try:
            result = eval(result_str)
        except NameError as e:
            try:
                result = json.loads(result)
            except ValueError as e:
                error_msg += '\nError handle result', result
        if error_msg:
            print error_msg
        result.update({'test': '', 'error': error_msg})
        return result
    
    def _create_grade_volume(self):
        tmp_volume_name = '%030x' % random.randrange(16**30)  # random 64-base string of length 30
        tmp_volume_path = os.path.join('/tmp', tmp_volume_name)
        shutil.copytree(self.grader_root, tmp_volume_path)
        return tmp_volume_path

    def grade(self, payload, files, _):
        section_name, problem_name = payload.split('/')
        # checking the assignment
        try:
            gb.find_assignment(section_name):
        except Exception as e:
            if type(e).__name__ == "MissingEntry":
                error = 'Cannot find section', section_name
            else:
                error = str(e)
            return self._handle_result('{}', error)

        # create tmp volume for docker
        tmp_volume_path = self._create_grade_volume()
        volume_setting = {tmp_volume_path: {'bind': self.grader_root, 'mode': 'rw'}}
        files = json.loads(files)
        submission_url = files.values()[0]

        command_str = 'python2.7 grade.py {} {} {}'.format(section_name, problem_name, submission_url)
        c = docker.from_env()
        result_str = c.containers.run(DOCKER_IMAGE, remove=True, command=command_str, volumes=volume_setting)
        return self._handle_result(result_str)

if __name__ == "__main__":
    d = DockerGrader()
    sample_nb = 'https://raw.githubusercontent.com/jupyter/nbgrader/master/nbgrader/docs/source/user_guide/source/ps1/problem1.ipynb'
    print '********* dummy test *********'
    print d.grade('ps1/problem1', '{"problem1.ipynb": "http://asdf.com"}', '')
    print '********* grading test *********'
    print d.grade('ps1/problem1', '{{"problem1.ipynb": "{}"}}'.format(sample_nb), '')
