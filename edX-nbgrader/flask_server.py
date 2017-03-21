from flask import Flask, request
import json

def grade(problem, student_response):
    #TODO: error handling, problem specification, unique student name
    randfilename = randgen()
    grading_dir = 'submitted/hacker/ps1/'
    feedback_html = 'feedback/hacker/ps1/problem1.html'
    score = None

    # Create python file to be tested from student's submitted program
    program_name = "problem1.ipynb"
    try:
        with open(grading_dir + program_name,'w') as f:
            for l in urllib.urlopen(student_response):
                f.write(l)
    except:
        msg = 'invalid link'
        return process_result(msg, score)
    p = subprocess.Popen(["nbgrader", "autograde", "ps1", "--student", "hacker"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    print "Out is: >>>\n{0}\n<<<".format(out)
    print "Err is: >>>\n{0}\n<<<".format(err)
    if 'AutogradeApp | ERROR' not in err:
        os.system('nbgrader feedback ps1 --student hacker')
    else:
        msg = 'There is some problem during grading'
        return process_result(msg, score)

    with open(feedback_html, 'r') as f:
        soup = bs(''.join(f.readlines()), 'html.parser')
    report = soup.body.div.div.div
    report = [line.strip() for line in report.prettify().split('\n') if line and not line.strip().startswith('<')]
    report = [l for l in report if not l.startswith('Comment')]  # We are not going to provide manual comment

    #remove student's program from disk
    os.remove(grading_dir + program_name)
    os.remove(feedback_html)
    
    score = float(report[0].split(' ')[-3])
    msg = '\n'.join(report)
    return process_result(msg, score)
    
    
def process_result(msg, score):
    if score is not None:
        correct = score > 0
    correct = None
    return {'msg': msg, 'score': score, 'correct': correct}


def get_info(data):
    # print body_content
    xqueue_body = json.loads(data["xqueue_body"])
    problem = json.loads(xqueue_body["grader_payload"])
    student_response = xqueue_body["student_response"]
    return problem, student_response

"""
Server & Request handler
"""

app = Flask(__name__)

@app.route("/")
def index():
    return "This is the grader server for CSE255 Spring 2017."

@app.route("/submit/", methods=['POST'])
def submit():
    data = request.get_json()
    print json.dumps(data)
    problem, student_response = get_info(data)
    result = grade(problem, student_response)
    print result
    self.send_response(200)
    self.end_headers()
    self.wfile.write(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
