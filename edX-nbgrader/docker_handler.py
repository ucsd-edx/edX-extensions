import requests
import docker
import subprocess
from time import sleep
import json

class DockerHandler:
    def __init__(self, ip='localhost', port=4000, grader_image='zhipengyan/ucsdx:simple_grader'):
        """
        grader object
        :param grader_root: course directory
        """
        self.port = port
        self.ip = ip
        self.grade_url = 'http://{}:{}/grade'.format(ip, port)
        self.shutdown_url = 'http://{}:{}/shutdown'.format(ip, port)
        self.grader_image = grader_image

        self.client = docker.from_env()

    def __call__(self, request_json):
        p = subprocess.Popen(["docker", "run", '-t', '-p', '{}:80'.format(self.port),
                              self.grader_image], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(1)
        try:
            r = requests.post(self.grade_url, json=request_json)
            results = json.loads(r.text)
        # out, err = p.communicate()
        except Exception as e:
            raise e
        finally:
            _ = requests.post(self.shutdown_url)
        return results

if __name__ == '__main__':
    test_json = {"xqueue_files": "{\"problem1.ipynb\": \"http://google.com\"}", "xqueue_body": "{\"grader_payload\": \"ps1\"}"}
    dh = DockerHandler()
    print dh(test_json)
