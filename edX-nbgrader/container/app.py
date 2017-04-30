"""
Docker container server to handle individual submission
Usage: Gets submission url through HTTP POST from the grader_server
    Invokes simple_grader to process the submission
Author: Zhipeng Yan
Date: Apr 30 2017
"""

from docker_grader import SimpleGrader
from flask import Flask, request, jsonify
import os
import json
from simple_grader import SimpleGrader


app = Flask(__name__)
grader = SimpleGrader('/home/ubuntu/edX-extensions/edX-nbgrader/container/')


def shutdown():
    raise RuntimeError("finish grading")


@app.route("/grade", methods=['POST'])
def grade():
    data = request.get_json(force=True)
    xqueue_body = json.loads(data['xqueue_body'])
    section_name = xqueue_body['grader_payload']  # ps1
    submission_files = json.loads(data['xqueue_files'])
    submission_url = submission_files['problem1.ipynb']

    try:
        feedback = grader.grade(section_name, submission_url)
        return jsonify(feedback)
    except Exception, msg:
        print 'Internal Error:', msg
        return jsonify({'msg': msg})
    finally:
        shutdown()


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80)
    except RuntimeError, msg:
        if msg == 'finish grading':
            pass
        else:
            raise RuntimeError(msg)
