import subprocess
import sys

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    user_input = "foo && cat /etc/passwd" # value supplied by user
    subprocess.call("grep -R {} .".format(user_input), shell=True)
    return 'Just a quick hello-world'

