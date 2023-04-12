from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def hello_world():
    
    return ("<p>Hello, World!</p>")

# if __name__ == '__main__':
#     app.run(host='"sla302.cs.uky.edu', port=9999, debug=True)

@app.route("/api/getteam", methods=['GET','POST'])
def getteam():
    #to address MF1 in the assignment
    project_status = { "team_name": "Daniel and Sandesh",
    "members": ["912333054", "912270286"],
    "app_status_code": 1,
    }
    return (render_template('getteam.html',
                            project_status=project_status))

@app.route("/api/reset")
def reset():
    #To address MF2 in the assignment
    # code 0 = my data could not be reset, 1 = my data was reset
    #TODO: change this when resetting is implemented
    isReset = 0
    reset_status = {"reset_status_code":isReset}
    return(render_template('reset.html',reset_status = json.dumps(reset_status)))

@app.route("/api/zipalertlist")
def zipalertlist():
    #To address RTR1 in the assignment
    #TODO: have this call a function in the controller which returns the list of zip codes
    
    ziplist = {"ziplist": [40351,40513,40506]}

    return (render_template('zipalertlist.html', ziplist = json.dumps(ziplist)))

@app.route("/api/alertlist")
def alertlist():
    #To address RTR2 in the assignment
    #code 0 = state is not in alert, 1 = state is in alert
    #TODO: have this call a function in the controller which decides if a state is in alert or not

    state_status = {"state_status": 0}

    return (render_template('state_status.html', state_status = json.dumps(state_status)))